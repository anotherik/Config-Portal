# Config Portal – Software Composition Analysis (SCA) Demonstration

> ✅ **This branch contains the secure version of Config-Portal**, using `yaml.safe_load()` and updated dependencies to prevent YAML deserialization vulnerabilities.
> 
> If you're looking for the vulnerable version to test and demonstrate SCA tools, switch to the [`main` branch](../../tree/main).

**Config Portal** is a purposely vulnerable Python Flask web application that simulates a lightweight internal tool used by development teams to import and preview YAML-based project configuration files. These configurations typically define metadata like project name, environment, and setup scripts.

This project is designed to demonstrate **Software Composition Analysis (SCA)** in action by showing how known vulnerable dependencies (like `pyyaml==5.1`) can be identified, exploited, and remediated using open-source security tools.

## 🧾 Example Config Input

Below is a sample YAML configuration that a developer might upload through Config Portal. It defines metadata for a project, deployment preferences, and contact information.

```
project: threatbyte
version: 1.0.3
environment: staging
settings:
  auto_rollback: true
  max_retries: 3
  enable_telemetry: false
  notifications:
    slack_channel: "#deployments"
    contacts:
      - alice@example.com
      - bob@example.com
pre_deploy:
  - echo "Running database migrations..."
  - ./scripts/backup.sh
post_deploy:
  - ./scripts/notify.sh
  - echo "Deployment complete."
```

## 🎯 Purpose

This app serves as a real-world case study to:

- Show how insecure use of `yaml.load()` introduces critical vulnerabilities  
- Demonstrate how to identify such risks using SCA tools  
- Exploit the vulnerability with real YAML payloads  
- Apply and verify secure remediation  


## 🚀 Features

- Simulates a DevOps-style YAML config uploader  
- Uses `PyYAML==5.1`, vulnerable to multiple CVEs  
- Allows testing of payloads like `!!python/object/apply` and `!!python/object/new`  
- Highlights the importance of dependency scanning  


## ⚠️ CVEs Demonstrated (fixed in this branch)

| CVE ID         | Description                                               |
|----------------|-----------------------------------------------------------|
| CVE-2017-18342 | Arbitrary object deserialization with `yaml.load()`       |
| CVE-2019-20477 | Incomplete fix allowing exploitation via `Popen` class    |
| CVE-2020-1747  | Unsafe behavior in `FullLoader` with `object/new`         |


## 🏗️ Setup

### 1. Clone the repo

```
git clone https://github.com/YOUR-USERNAME/ConfigPortal.git
cd ConfigPortal
```

### 2. Create a virtual environment

```
python3 -m venv venv
source venv/bin/activate
```

### 3. Install the dependencies

```
pip install -r requirements.txt
```

## Run the Application

```
python app.py
```

Then open your browser at: [http://localhost:5000](http://localhost:5000)


## 🧪 Exploit Example (fixed in this branch)

Paste this into the form:

```
!!python/object/apply:subprocess.check_output [["id"]]
```

Expected message: Rejected unsafe YAML content: potential exploit blocked.

## 🔍 Scan with SCA Tools

### OSV-Scanner

```
osv-scanner --lockfile=requirements.txt
```

### Trivy

```
trivy fs --scanners vuln .
```

## 📜 License

This project is intended for **educational use only**.

