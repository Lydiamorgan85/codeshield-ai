# CI/CD Integration Guide

Integrate CodeShield AI into your continuous integration and deployment pipelines.

## GitHub Actions

### Basic Security Scan

Create `.github/workflows/codeshield.yml`:

```yaml
name: CodeShield Security Scan

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main ]

jobs:
  security-scan:
    runs-on: ubuntu-latest
    
    steps:
    - name: Checkout code
      uses: actions/checkout@v3
    
    - name: Setup Node.js
      uses: actions/setup-node@v3
      with:
        node-version: '18'
    
    - name: Install CodeShield AI
      run: |
        git clone https://github.com/Lydiamorgan85/codeshield-ai.git
        cd codeshield-ai
        npm install
    
    - name: Run Security Scan
      run: npx codeshield analyze ./src --output report.json
    
    - name: Upload Report
      uses: actions/upload-artifact@v3
      if: always()
      with:
        name: security-report
        path: report.json
    
    - name: Fail on Critical Issues
      run: npx codeshield analyze ./src --fail-on-critical
```

### Advanced Configuration with PR Comments

```yaml
name: CodeShield PR Review

on:
  pull_request:

jobs:
  security-review:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Run CodeShield
      id: scan
      run: |
        npx codeshield analyze ./src --format github-comment > comment.txt
    
    - name: Comment on PR
      uses: actions/github-script@v6
      with:
        script: |
          const fs = require('fs');
          const comment = fs.readFileSync('comment.txt', 'utf8');
          github.rest.issues.createComment({
            issue_number: context.issue.number,
            owner: context.repo.owner,
            repo: context.repo.repo,
            body: comment
          });
```

## GitLab CI

Create `.gitlab-ci.yml`:

```yaml
stages:
  - security

codeshield_scan:
  stage: security
  image: node:18
  
  script:
    - git clone https://github.com/Lydiamorgan85/codeshield-ai.git
    - cd codeshield-ai && npm install && cd ..
    - npx codeshield analyze ./src --output report.json
  
  artifacts:
    reports:
      junit: report.json
    paths:
      - report.json
    expire_in: 1 week
  
  only:
    - merge_requests
    - main
```

## Jenkins Pipeline

Create `Jenkinsfile`:

```groovy
pipeline {
    agent any
    
    stages {
        stage('Security Scan') {
            steps {
                script {
                    sh '''
                        git clone https://github.com/Lydiamorgan85/codeshield-ai.git
                        cd codeshield-ai
                        npm install
                        npx codeshield analyze ../src --output report.json
                    '''
                }
            }
        }
        
        stage('Publish Report') {
            steps {
                publishHTML([
                    reportDir: 'codeshield-ai',
                    reportFiles: 'report.html',
                    reportName: 'Security Report'
                ])
            }
        }
        
        stage('Quality Gate') {
            steps {
                script {
                    sh 'npx codeshield analyze ./src --fail-on-critical'
                }
            }
        }
    }
    
    post {
        always {
            archiveArtifacts artifacts: '**/report.json', allowEmptyArchive: true
        }
    }
}
```

## CircleCI

Create `.circleci/config.yml`:

```yaml
version: 2.1

jobs:
  security-scan:
    docker:
      - image: cimg/node:18.0
    
    steps:
      - checkout
      
      - run:
          name: Install CodeShield AI
          command: |
            git clone https://github.com/Lydiamorgan85/codeshield-ai.git
            cd codeshield-ai
            npm install
      
      - run:
          name: Run Security Scan
          command: npx codeshield analyze ./src --output report.json
      
      - store_artifacts:
          path: report.json
          destination: security-report

workflows:
  version: 2
  security-workflow:
    jobs:
      - security-scan
```

## Azure DevOps

Create `azure-pipelines.yml`:

```yaml
trigger:
  - main

pool:
  vmImage: 'ubuntu-latest'

steps:
- task: NodeTool@0
  inputs:
    versionSpec: '18.x'

- script: |
    git clone https://github.com/Lydiamorgan85/codeshield-ai.git
    cd codeshield-ai
    npm install
  displayName: 'Install CodeShield AI'

- script: |
    npx codeshield analyze ./src --output $(Build.ArtifactStagingDirectory)/report.json
  displayName: 'Run Security Scan'

- task: PublishBuildArtifacts@1
  inputs:
    pathToPublish: '$(Build.ArtifactStagingDirectory)'
    artifactName: 'security-reports'
```

## Docker Integration

### Dockerfile for CodeShield

```dockerfile
FROM node:18-alpine

WORKDIR /app

RUN git clone https://github.com/Lydiamorgan85/codeshield-ai.git . && \
    npm install

ENTRYPOINT ["npx", "codeshield"]
CMD ["analyze", "/code"]
```

### Usage

```bash
# Build image
docker build -t codeshield:latest .

# Scan your code
docker run -v $(pwd):/code codeshield:latest analyze /code
```

## Environment Variables

Configure via environment variables:

```bash
# CI/CD pipeline configuration
export CODESHIELD_SEVERITY=critical,high
export CODESHIELD_OUTPUT_FORMAT=json
export CODESHIELD_FAIL_ON_ISSUES=true
export CODESHIELD_EXCLUDE="node_modules/**,dist/**"
```

## Fail Conditions

### Fail on Any Critical Issue

```bash
npx codeshield analyze ./src --fail-on-critical
```

### Fail on Severity Threshold

```bash
npx codeshield analyze ./src --max-critical 0 --max-high 5
```

### Custom Exit Codes

```bash
npx codeshield analyze ./src --exit-code-critical 1 --exit-code-high 2
```

## Notifications

### Slack Integration

```yaml
- name: Notify Slack
  if: failure()
  uses: slackapi/slack-github-action@v1
  with:
    payload: |
      {
        "text": "Security scan failed! Check the report."
      }
  env:
    SLACK_WEBHOOK_URL: ${{ secrets.SLACK_WEBHOOK }}
```

### Email Notifications

```yaml
- name: Send Email
  if: failure()
  uses: dawidd6/action-send-mail@v3
  with:
    server_address: smtp.gmail.com
    server_port: 465
    username: ${{ secrets.MAIL_USERNAME }}
    password: ${{ secrets.MAIL_PASSWORD }}
    subject: CodeShield Security Alert
    body: Security vulnerabilities detected in latest commit
    to: team@example.com
    from: ci@example.com
```

## Performance Tips

### Cache Dependencies

```yaml
- name: Cache node modules
  uses: actions/cache@v3
  with:
    path: ~/.npm
    key: ${{ runner.os }}-node-${{ hashFiles('**/package-lock.json') }}
```

### Parallel Scans

```yaml
strategy:
  matrix:
    directory: ['./src', './tests', './lib']
    
steps:
  - run: npx codeshield analyze ${{ matrix.directory }}
```

### Incremental Scanning

```bash
# Only scan changed files
git diff --name-only HEAD~1 | xargs npx codeshield analyze
```

## Troubleshooting

**Issue: Pipeline times out**
```yaml
# Increase timeout
timeout-minutes: 30
```

**Issue: Too many false positives**
```bash
# Adjust sensitivity
npx codeshield analyze --severity critical,high
```

**Issue: Large repositories slow**
```bash
# Use parallel processing
npx codeshield analyze --parallel 4
```

## Best Practices

1. **Run on every PR** - Catch issues before merge
2. **Fail on critical issues** - Enforce security standards
3. **Archive reports** - Track security trends over time
4. **Notify team** - Alert on new vulnerabilities
5. **Regular updates** - Keep CodeShield AI current

## Support

Questions about CI/CD integration?
- Check [Troubleshooting Guide](troubleshooting.md)
- Open an issue on GitHub
- Email: lydiamorgan000@gmail.com
