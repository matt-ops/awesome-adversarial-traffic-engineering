import fs from "node:fs";
import http2, { type ServerHttp2Session, type ServerHttp2Stream } from "node:http2";
import path from "node:path";
import readline from "node:readline";
import type { TLSSocket } from "node:tls";

type Arguments = {
  host: string;
  port: number;
  cert: string;
  key: string;
  output: string;
  maxConnections: number;
  maxStreams: number;
  timeoutMs: number;
};

type Observation = {
  session_id: number;
  negotiated_alpn: string;
  remote_settings: http2.Settings;
  stream_count: number;
  stream_ids: number[];
  clients: string[];
  request_header_sets: string[][];
  missing_fields: string[];
};

function fail(message: string): never {
  throw new Error(message);
}

function parseInteger(value: string | undefined, label: string): number {
  const parsed = Number(value);
  if (!Number.isInteger(parsed)) fail(`${label} must be an integer`);
  return parsed;
}

function parseArguments(argv: string[]): Arguments {
  const values = new Map<string, string>();
  for (let index = 0; index < argv.length; index += 2) {
    const name = argv[index];
    const value = argv[index + 1];
    if (!name?.startsWith("--") || value === undefined) fail("observer arguments must be --name value pairs");
    values.set(name, value);
  }
  const host = values.get("--host") ?? fail("--host is required");
  if (!new Set(["127.0.0.1", "localhost", "::1"]).has(host)) fail("observer host must be loopback");
  const port = parseInteger(values.get("--port"), "port");
  const maxConnections = parseInteger(values.get("--max-connections"), "max connections");
  const maxStreams = parseInteger(values.get("--max-streams"), "max streams");
  const timeoutMs = parseInteger(values.get("--timeout-ms"), "timeout");
  if (port < 0 || port > 65535) fail("port is outside its valid range");
  if (maxConnections < 1 || maxConnections > 4) fail("connection cap must be between 1 and 4");
  if (maxStreams < 1 || maxStreams > 8) fail("stream cap must be between 1 and 8");
  if (timeoutMs < 100 || timeoutMs > 30000) fail("timeout must be between 100 and 30000 ms");
  return {
    host,
    port,
    cert: values.get("--cert") ?? fail("--cert is required"),
    key: values.get("--key") ?? fail("--key is required"),
    output: values.get("--output") ?? fail("--output is required"),
    maxConnections,
    maxStreams,
    timeoutMs,
  };
}

const args = parseArguments(process.argv.slice(2));
const sessions = new Map<ServerHttp2Session, Observation>();
let connectionCount = 0;
let streamCount = 0;
let unexpectedCap = false;
let finishing = false;

const server = http2.createSecureServer({
  cert: fs.readFileSync(args.cert),
  key: fs.readFileSync(args.key),
  allowHTTP1: false,
  ALPNProtocols: ["h2"],
});

server.on("session", (session) => {
  connectionCount += 1;
  if (connectionCount > args.maxConnections) {
    unexpectedCap = true;
    session.destroy();
    return;
  }
  const socket = session.socket as TLSSocket;
  const observation: Observation = {
    session_id: connectionCount,
    negotiated_alpn: socket.alpnProtocol || "missing",
    remote_settings: session.remoteSettings,
    stream_count: 0,
    stream_ids: [],
    clients: [],
    request_header_sets: [],
    missing_fields: ["HTTP/2 header order is not exposed by this observer"],
  };
  sessions.set(session, observation);
  session.on("remoteSettings", (settings) => {
    observation.remote_settings = settings;
  });
  session.on("error", () => undefined);
});

server.on("stream", (stream: ServerHttp2Stream, headers) => {
  streamCount += 1;
  const session = stream.session as ServerHttp2Session | undefined;
  const observation = session ? sessions.get(session) : undefined;
  if (streamCount > args.maxStreams || observation === undefined) {
    unexpectedCap = true;
    stream.close(http2.constants.NGHTTP2_REFUSED_STREAM);
    return;
  }
  const client = String(headers["x-aate-client"] ?? "missing-client-tag");
  observation.stream_count += 1;
  observation.stream_ids.push(stream.id ?? 0);
  if (!observation.clients.includes(client)) observation.clients.push(client);
  observation.request_header_sets.push(Object.keys(headers).sort());
  stream.respond({
    ":status": 200,
    "content-type": "text/html; charset=utf-8",
    "cache-control": "no-store",
  });
  stream.end("<!doctype html><title>AATE local HTTP/2 observer</title><p>ok</p>");
});

server.on("error", (error) => {
  if (!finishing) {
    process.stderr.write(`${error.message}\n`);
    process.exitCode = 1;
  }
});

function finish(reason: string): void {
  if (finishing) return;
  finishing = true;
  for (const session of sessions.keys()) session.close();
  server.close(() => {
    const result = {
      status: unexpectedCap ? "cap-exceeded" : "observed",
      stop_reason: reason,
      bind: args.host,
      connection_count: connectionCount,
      stream_count: streamCount,
      sessions: [...sessions.values()].sort((left, right) => left.session_id - right.session_id),
      explicit_missing_observations: [
        "HTTP/2 header ordering",
        "account identity",
        "intermediary behavior",
        "HTTP/3 and QUIC",
      ],
    };
    fs.mkdirSync(path.dirname(args.output), { recursive: true });
    fs.writeFileSync(args.output, `${JSON.stringify(result, null, 2)}\n`, {
      encoding: "utf8",
      mode: 0o600,
    });
    if (unexpectedCap) process.exitCode = 2;
  });
}

server.listen(args.port, args.host, () => {
  const address = server.address();
  if (address === null || typeof address === "string") fail("observer did not receive a TCP address");
  process.stdout.write(`${JSON.stringify({ status: "ready", host: args.host, port: address.port })}\n`);
});

const input = readline.createInterface({ input: process.stdin });
input.on("line", (line) => {
  if (line === "STOP") finish("parent-requested-cleanup");
});

setTimeout(() => finish("wall-clock-timeout"), args.timeoutMs).unref();
