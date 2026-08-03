# Required Branch Protection

Open **Settings -> Branches -> Branch protection rules** in the GitHub
repository and create or edit the rule for `main`. Enable **Require a pull
request before merging** and **Require status checks to pass before merging**.
Select the two auth-service status checks named exactly `lint` and `test`.

The data-service equivalents, `lint-data-service` and `test-data-service`,
should also be required after the capstone jobs have run at least once. Keep
the branch up to date before merging so every required result applies to the
actual merge commit.
