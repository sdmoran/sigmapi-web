# Sigma Pi, Gamma Iota Chapter Website: Deployment

[_(Back to developer guide)_](https://github.com/sigmapi-gammaiota/sigmapi-web/tree/master/docs/dev-guide/index.md)

## Deploying to WebFaction

### 1. SSH into our WebFaction box.

Credentials are redacted, contact @thomas-schweich if you need them.

```bash
$ ssh our_username@our_domain.webfactional.com
```

### 2. Navigate to the deploy folder, and run the deploy script.

```bash
$ cd deploy
$ ./deploy.sh
```

Note that the `deploy.sh` script in that folder should be a copy of the one in this repository. It is kept here for version controlling.

At this point you should be *done*, unless you need to...

### 3. Rollback if necessary

There may be warnings on deploy, but if there is a failure in production after deployment then you should perform a rollback. In the same directory as the `delpoy.sh` script is `rollback.sh`, which will revert production to its previous deploy.

Note that there are additional complications if you wish to deploy a code change which requires a database migration. For now defer to @thomas-schweich for that.
