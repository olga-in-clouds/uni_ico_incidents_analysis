import kagglehub

# Download latest version
path = kagglehub.dataset_download("rorycaley/ico-data-security-incidents")

print("Path to dataset files:", path)