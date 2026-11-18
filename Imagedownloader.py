import urllib.request

url = "https://images.unsplash.com/photo-1501785888041-af3ef285b470?auto=format&fit=crop&w=1200&q=80"
output_path = "mountains.jpg"

try:
    with urllib.request.urlopen(url) as response, open(output_path, "wb") as file:
        file.write(response.read())
    print(f"Image downloaded successfully as {output_path}")
except Exception as error:
    print(f"Download failed: {error}")
