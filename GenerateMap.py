import os
MAP_DIR = "generated_maps"

def generate_tcc_map(input_data_path):
    os.makedirs(MAP_DIR, exist_ok=True)

    base_name = os.path.basename(input_data_path)
    output_filename = os.path.splitext(base_name)[0] + ".png"
    output_map_path = os.path.join(MAP_DIR, output_filename)

    if os.path.exists(output_map_path):
        print(f"✔️ Map already exists: {output_filename}. Skipping generation.")
        return output_map_path

    print(f"⚙️ Generating map for: {base_name}...")
    try:
        with open(output_map_path, 'w') as f:
            f.write("This is a dummy map.")

        print(f"✅ Map generated: {output_filename}")
        return output_map_path

    except Exception as e:
        print(f"❌ Failed to generate map for {base_name}. Error: {e}")
        return None

#Example:
if __name__ == "__main__":
    data_file_path = "insat_data/INSAT3D_IRBRT_20240701_1200.H5" 
    
    os.makedirs(os.path.dirname(data_file_path), exist_ok=True)
    if not os.path.exists(data_file_path):
        with open(data_file_path, 'w') as f: f.write("dummy data")
            
    generate_tcc_map(data_file_path)
    generate_tcc_map(data_file_path)
