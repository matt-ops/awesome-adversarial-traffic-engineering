self.addEventListener("message", () => {
  self.postMessage({
    language: self.navigator.language,
    hardwareConcurrency: self.navigator.hardwareConcurrency,
  });
});
