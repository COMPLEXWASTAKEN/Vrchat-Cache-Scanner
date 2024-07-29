from core import *

def parse_avatar_ids_from_cache(cache_dir, output_file):
    avatar_ids = load_existing_avatar_ids(output_file)

    try:
        for directory in os.listdir(cache_dir):
            if os.path.isdir(os.path.join(cache_dir, directory)):
                for subdirectory in os.listdir(os.path.join(cache_dir, directory)):
                    if os.path.isdir(os.path.join(cache_dir, directory, subdirectory)):
                        data_file_path = os.path.join(
                            cache_dir, directory, subdirectory, '__data')
                        try:
                            with open(data_file_path, 'r', encoding='utf-8', errors='ignore') as file:
                                file_content = file.read()
                                matches = re.findall(
                                    r'avtr_\w{8}-\w{4}-\w{4}-\w{4}-\w{12}', file_content)
                                for avatar_id in matches:
                                    if avatar_id not in avatar_ids:
                                        log.debug(f"[Found avatar ID: {avatar_id}]")
                                        avatar_ids.append(avatar_id)
                                        save_avatar_ids(avatar_ids, output_file)
                                    else:
                                        log.debug(f"[Duplicate avatar ID: {avatar_id}]")
                                    break
                                
                        except Exception as e:
                            log.failure(f"Error reading {data_file_path}: {str(e)}")
    except Exception as e:
        raise ValueError(f"Error reading cache directory {cache_dir}: {str(e)}")

    return avatar_ids

def get_avatar_data(avatar_id):
    res = requests.get(f"https://api.vrchat.cloud/api/1/avatars/{avatar_id}", headers={
        "X-Unity-Version": "2019.4.40f1",
        "X-Platform": "standalonewindows",
        "Accept": "*/*",
        "user-agent": "UnityPlayer/2022.3.6f1-DWR (UnityWebRequest/1.0, libcurl/7.80.0-DEV)",
    })
    if res.status_code == 429:
        log.failure(f"Failed to get avatar data for avatar ID {avatar_id}: Rate limited")
    elif res.status_code == 404:
        log.failure(f"Avatar ID {avatar_id} not found")
    else:
        return res.json() if res.status_code == 200 else None

def load_existing_avatar_ids(file_path):
    if os.path.exists(file_path):
        with open(file_path, 'r') as json_file:
            return json.load(json_file)
    return []

def save_avatar_ids(avatar_ids, file_path='avatar_ids.json'):
    with open(file_path, 'w') as json_file:
        json.dump(avatar_ids, json_file, indent=4)

def save_avatar_data(avatar_data_list, file_path='avatar_data.json'):
    with open(file_path, 'w') as json_file:
        json.dump(avatar_data_list, json_file, indent=4)

def main():
    colorama.init()
    pc_user = os.getlogin()
    cache_dir = f'C:/Users/{pc_user}/AppData/LocalLow/VRChat/VRChat/Cache-WindowsPlayer'
    avatar_ids_file = 'avatar_ids.json'
    avatar_ids = []

    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = [executor.submit(parse_avatar_ids_from_cache, cache_dir, avatar_ids_file)]
        for future in concurrent.futures.as_completed(futures):
            avatar_ids.extend(future.result())

    if not avatar_ids:
        log.failure("No avatar IDs found.")
        return

    avatar_data_list = []

    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = {executor.submit(get_avatar_data, avatar_id): avatar_id for avatar_id in avatar_ids}
        for future in concurrent.futures.as_completed(futures):
            avatar_data = future.result()
            if avatar_data:
                avatar_data_list.append(avatar_data)

    save_avatar_data(avatar_data_list)
    log.info(f"Total Avatars Retrieved: {len(avatar_data_list)}")
    log.ask("Press Enter To Exit")

if __name__ == "__main__":
    main()
