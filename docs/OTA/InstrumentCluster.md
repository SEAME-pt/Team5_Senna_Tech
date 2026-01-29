
## How to release a new version (Instrument Cluster)
The release process is triggered automatically whenever a new tag following the pattern clusterqt-v* is pushed to the repository.

### Pipeline Stages
1-  Checkout: Pulls the source code including Git LFS assets.

2 - Build: Creates a Docker environment to cross-compile the Qt application.

3 - Extraction: Pulls the compiled appcar_cluster binary from the container.

4 - Packaging: Compresses the binary and generates a SHA256 checksum for verification.

5 - Publishing: Creates a GitHub Release and attaches the artifacts.

## Step-by-Step: Triggering a New Release

- Follow these steps to release a new version of the software.

#### 1. Pre-requisites
- Ensure all code changes are committed and pushed to the main or develop branch.

- Verify that the docker/Dockerfile is updated if there are new dependencies.

#### 2. Create and Push a Version Tag
- The GitHub Action specifically looks for tags starting with clusterqt-v. Use semantic versioning (e.g., v1.0.2).

- Open your terminal and run:


# Example for version 1.2.0
```
git tag -a clusterqt-v1.2.0 -m "Release version 1.2.0: Summary of key changes"
git push origin clusterqt-v1.2.0
```
#### 3. Monitor the Build
- Navigate to the Actions tab in the GitHub repository.

- Select the Release workflow from the left sidebar.

- Click on the running job to view logs. The job runs on a self-hosted Linux X64 runner with Docker support.

#### 4. Verify the Release
Once the workflow finishes successfully:

- Go to the Releases section on the repository homepage.

- Check for the new entry titled ClusterQT clusterqt-vX.Y.Z.

- Ensure the following assets are present:

- appcar_cluster.tar.gz (The executable)

- appcar_cluster.tar.gz.sha256 (Checksum for integrity)