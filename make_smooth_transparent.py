from PIL import Image

def process_logo(input_path, output_path):
    try:
        img = Image.open(input_path).convert("RGBA")
        
        # We will do a simple flood-fill to make the outer white background transparent.
        # This prevents turning the white pixels inside the robot into transparent holes.
        width, height = img.size
        pixels = img.load()
        
        # Start at (0,0) assuming it's the background
        start_color = pixels[0, 0]
        
        # We treat any pixel close to start_color (white) as background
        def is_bg(c):
            # c is (r,g,b,a)
            return all(abs(c[i] - start_color[i]) < 15 for i in range(3))
            
        stack = [(0,0), (width-1, 0), (0, height-1), (width-1, height-1)]
        visited = set(stack)
        
        while stack:
            x, y = stack.pop()
            if is_bg(pixels[x, y]):
                pixels[x, y] = (255, 255, 255, 0)
                
                # Check neighbors
                for dx, dy in [(0,1), (1,0), (0,-1), (-1,0)]:
                    nx, ny = x + dx, y + dy
                    if 0 <= nx < width and 0 <= ny < height and (nx, ny) not in visited:
                        visited.add((nx, ny))
                        stack.append((nx, ny))

        # Pass 2: Clean up anti-aliasing edges (white halos) that were left behind
        # by making near-white pixels that touch transparent pixels slightly transparent.
        for _ in range(2):
            to_weaken = []
            for y in range(1, height-1):
                for x in range(1, width-1):
                    p = pixels[x, y]
                    if p[3] > 0 and is_bg(p): # A whiteish pixel that wasn't touched by flood-fill
                        # If touching a transparent pixel
                        if (pixels[x+1,y][3] == 0 or pixels[x-1,y][3] == 0 or 
                            pixels[x,y+1][3] == 0 or pixels[x,y-1][3] == 0):
                            to_weaken.append((x,y))
            for x, y in to_weaken:
                pixels[x, y] = (255, 255, 255, 0)

        img.save(output_path, "PNG")
        print("Smooth flood-filled transparent PNG saved to:", output_path)

    except Exception as e:
        print("Error:", e)

if __name__ == "__main__":
    process_logo('logo1.png', 'logo1_transparent.png')
