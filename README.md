# README: KnowledgeGraphAttribution Repository

This repository contains the implementation of methods and experiments presented in the paper: ["ClaimVer: Explainable Claim-Level Verification and Evidence Attribution of Text Through Knowledge Graphs"](https://arxiv.org/pdf/2403.09724) . The codebase is distributed across multiple VMs and involves components built with Node.js, Python, and Java. Follow the steps below to set up and use the repository.

Paper Link: https://aclanthology.org/2024.findings-emnlp.795/

ClaimVer LLM Weights: https://huggingface.co/preetam7

Citation: Dammu, Preetam Prabhu Srikar, et al. "ClaimVer: Explainable Claim-Level Verification and Evidence Attribution of Text Through Knowledge Graphs." arXiv preprint arXiv:2403.09724 (2024).



## Prerequisites

### Software Installation
1. **Node.js**
   - Install the required Node.js version.
   - [How to install older versions of Node.js](https://stackoverflow.com/questions/23691194/how-to-install-older-version-of-node-js-on-windows).

2. **Java**
   - Download and install JDK 11.
   - [JDK 11 Archive Downloads](https://www.oracle.com/java/technologies/javase/jdk11-archive-downloads.html).
   - Set up Eclipse IDE for Java development:
     - [Eclipse Downloads](https://www.eclipse.org/downloads/packages/release/2022-06/r).
     - Troubleshoot compiler issues: [Stack Overflow guide](https://stackoverflow.com/questions/31916579/eclipse-says-jre-does-not-support-the-current-compiler-level-of-1-8-but-it-is-se).

3. **Python**
   - Install Python (any version). Ensure it is added to your system's PATH.

### Conda Environment Setup (Recommended)
1. Create a new conda virtual environment:
   ```bash
   conda create -n kgattribution_env python=3.x
   conda activate kgattribution_env
   ```

2. Install required Python packages:
   ```bash
   pip install -r requirements.txt
   ```

3. Download the SpaCy language model:
   ```bash
   python -m spacy download en_core_web_md
   ```

## Repository Structure

### Key Components
- **Frontend**: Contains the user interface built with Node.js.
- **Backend**: Includes Python scripts for graph traversal and attribution.
- **Java Module**: Implements graph querying and processing logic, located in `rdf-entity-path`.
- **Utilities**: Helper scripts for handling Python-Java integration.

## Setup Steps

### 1. Clone the Repository
```bash
git clone https://github.com/TinSlim/WD-PathFinder.git
```

### 2. Frontend Setup
Navigate to the `/frontend` directory and install dependencies:
```bash
cd frontend
npm install
```

### 3. Load Java Code
- Load the `rdf-entity-path` project into Eclipse IDE.
- Do not run it yet, as it requires graph data to function properly.

### 4. Graph Data Setup
1. **Download the Required Wikidata Dump File**
   - [Guide to Importing Wikidata Dumps](https://topicseed.com/blog/importing-wikidata-dumps/).
   - Use the older, smaller dump file from Zenodo: [Zenodo Record](https://zenodo.org/records/4282941).
   - Note: Downloads are rate-limited to 5 MBps.

2. **Move and Convert the Dump File**
   - Place the compressed `.bz2` file into `./python/prearchivo`.
   - Convert the `.bz2` file to `.gzip` in chunks due to memory constraints.

### 5. Python Integration
The Python-Java interaction is handled via the `utils.woolnet_pipe` module. Ensure all dependencies are installed and the Python environment is configured correctly.
