# Publish checklist

- [ ] Secret scan completed
- [ ] Employer-confidentiality review completed
- [ ] Internal link validation completed
- [ ] External primary-source links sampled
- [ ] License and attribution reviewed
- [ ] Screenshots contain only synthetic/local data
- [ ] Fixture and sample-data review completed
- [ ] Local-target and load-ceiling safety tests pass
- [ ] README and one-path navigation reviewed
- [ ] Documentation build is reproducible
- [ ] No remote is configured

Only after all checks pass may a human create a public remote. Suggested human-run sequence: review `git status`, create the repository in the chosen hosting UI, add the remote, review the push refspec, and push. These steps are intentionally not automated here.

