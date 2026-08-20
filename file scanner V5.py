import os
import time
import json

# next feature: NL file search, multi-request, smart file open, voice input,
# Bengali understanding, spelling correction, user permissions, file preview,
# search ranking, desktop app, cloud access, real DB, API backend, web/mobile UI

HISTORY_FILE = "history.json"


def build_criteria():
    return {"keyword": None, "year": None, "month": None,
            "file_type": None, "location": None, "search_text": None}


def reset_criteria():
    return build_criteria()


def set_criteria(criteria, keyword=None, year=None, month=None,
                  file_type=None, location=None, search_text=None):
    criteria["keyword"] = keyword
    criteria["year"] = year
    criteria["month"] = month
    criteria["file_type"] = file_type
    criteria["location"] = location
    criteria["search_text"] = search_text
    return criteria


criteria = build_criteria()


def save_history(history):
    try:
        with open(HISTORY_FILE, "w") as file:
            json.dump(history, file, indent=4)
    except OSError:
        print("Could not save history.")


def load_history():
    try:
        with open(HISTORY_FILE, "r") as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return []


history = load_history()


def add_history(search):
    history.append(search)
    if len(history) > 50:
        history.pop(0)
    save_history(history)


def clear():
    os.system("cls" if os.name == "nt" else "clear")


def normalize_file_type(file_type):
    if file_type is None:
        return None
    return str(file_type).lower().strip().lstrip(".")


def get_integer(prompt):
    value = input(prompt).strip()
    if value == "":
        return None
    try:
        return int(value)
    except ValueError:
        print("⚠️ Please enter a number.")
        return None


def search_folder(search, location=None):
    results = []
    if not search:
        return results
    if location is None:
        location = "/storage/emulated/0"
    if not os.path.exists(location):
        return results

    search = search.lower().strip()
    for all_folder, folders, files in os.walk(location):
        for folder_name in folders:
            if search in folder_name.lower():
                path = os.path.join(all_folder, folder_name)
                results.append({"kind": "folder", "name": folder_name, "path": path})
    return results


def src_files(criteria):
    """Main file search engine. Filters: keyword, year, month, file_type, location, search_text."""
    results = []
    keyword = criteria.get("keyword")
    year_filter = criteria.get("year")
    month_filter = criteria.get("month")
    file_type_filter = criteria.get("file_type")
    location = criteria.get("location") or "/storage/emulated/0"

    if keyword:
        keyword = str(keyword).lower().strip()
    if file_type_filter:
        file_type_filter = normalize_file_type(file_type_filter)

    if not os.path.exists(location):
        print("Location does not exist:", location)
        return results

    for all_folder, folders, files in os.walk(location):
        for file in files:

            if keyword and keyword not in file.lower():
                continue

            full_path = os.path.join(all_folder, file)

            try:
                size = os.path.getsize(full_path)
                modified = os.path.getmtime(full_path)
            except OSError:
                continue

            name, extension = os.path.splitext(file)
            file_type = extension.lower().lstrip(".")

            file_time = time.localtime(modified)
            year = file_time.tm_year
            month = file_time.tm_mon

            if year_filter is not None and year != year_filter:
                continue
            if month_filter is not None and month != month_filter:
                continue
            if file_type_filter is not None and file_type != file_type_filter:
                continue

            results.append({
                "kind": "file",
                "name": file,
                "path": full_path,
                "folder": all_folder,
                "size": size,
                "type": file_type,
                "modified": time.ctime(modified),
                "timestamp": modified
            })

    return results


def search_file(criteria):
    """Bridge between user/AI and search engine. Future AI layer calls this."""
    return src_files(criteria)


def multiple_search():
    criteria_list = []
    count = get_integer("How many searches do you want? ")
    if count is None or count <= 0:
        print("Invalid number.")
        return []

    for i in range(count):
        print(f"\n========== SEARCH {i + 1} ==========")
        criteria = reset_criteria()

        keyword = input("Keyword: ").strip() or None
        year = get_integer("Year: ")
        month = get_integer("Month: ")
        file_type = input("File type (pdf/txt/xlsx): ").strip() or None
        location = input("Location (blank = all storage): ").strip() or None

        set_criteria(criteria, keyword=keyword, year=year, month=month,
                     file_type=file_type, location=location)
        criteria_list.append(criteria)

    return criteria_list


def search_multiple(criteria_list):
    all_results = []
    if not criteria_list:
        return all_results
    for criteria in criteria_list:
        results = search_file(criteria)
        all_results.append({"criteria": criteria, "results": results})
    return all_results


def show_multiple_results(all_results):
    if not all_results:
        print("\n❌ No search requests.")
        return
    for i, item in enumerate(all_results, start=1):
        print("\n")
        print("========================================")
        print(f"        SEARCH REQUEST {i}")
        print("========================================")
        show_results(item["results"])


def open_file(path):
    if not os.path.exists(path):
        print("❌ File not found.")
        return False

    try:
        if os.name == "nt":
            os.startfile(path)
        else:
            command = f'am start -a android.intent.action.VIEW -d "file://{path}"'
            result = os.system(command)
            if result != 0:
                print("❌ Android could not open the file.")
                return False
        return True

    except Exception as error:
        print("❌ Could not open file.")
        print(error)
        return False


def find_matching_files(keyword, file_type=None):
    criteria = reset_criteria()
    set_criteria(criteria, keyword=keyword, file_type=file_type)
    return search_file(criteria)


def select_file(keyword, file_type=None):
    results = find_matching_files(keyword, file_type)

    if not results:
        print("\n❌ No matching file found.")
        return None

    if len(results) == 1:
        print("\n✅ One file found:")
        print(results[0]["name"])
        return results[0]

    print(f"\n📁 {len(results)} matching files found:")
    for i, result in enumerate(results, start=1):
        print(f"{i}. {result['name']} ({result['type']})")

    print("\nPlease choose a file.")
    choice = input("Enter number: ").strip()

    try:
        choice = int(choice)
    except ValueError:
        print("❌ Invalid choice.")
        return None

    if choice < 1 or choice > len(results):
        print("❌ Invalid file number.")
        return None

    return results[choice - 1]


def file_action(action, keyword, file_type=None):
    if action == "search":
        return find_matching_files(keyword, file_type)
    elif action == "open":
        return find_matching_files(keyword, file_type)
    else:
        print("\n❌ Unknown action:", action)
        return []


def open_files(results):
    if not results:
        print("\n❌ No files to open.")
        return

    print(f"\n📂 {len(results)} file(s) found.")

    if len(results) == 1:
        print("Opening:", results[0]["name"])
        open_file(results[0]["path"])
        return

    print("\nFiles:")
    for i, result in enumerate(results, start=1):
        print(f"{i}. {result['name']} ({result['type']})")

    confirm = input("\nOpen ALL these files? (y/n): ").strip().lower()
    if confirm != "y":
        print("❌ Opening cancelled.")
        return

    for result in results:
        print("Opening:", result["name"])
        open_file(result["path"])


def execute_file_action(action, keyword, file_type=None):
    results = file_action(action, keyword, file_type)
    if action == "search":
        show_results(results)
    elif action == "open":
        open_files(results)
    else:
        print("\n❌ Invalid action.")


def ask_ai(user_text):
    """AI Layer — OpenAI / Gemini / Claude will be connected here later."""
    print("\n[AI INPUT]")
    print(user_text)
    return None


def prepare_result(result, action):
    if not result:
        return None
    return {
        "action": action,
        "kind": result.get("kind"),
        "name": result.get("name"),
        "path": result.get("path"),
        "type": result.get("type"),
        "folder": result.get("folder"),
        "size": result.get("size"),
        "modified": result.get("modified")
    }


def prepare_results(results, action):
    return [data for r in results if (data := prepare_result(r, action))]


def create_command(action, keyword=None, year=None, month=None, file_type=None, location=None):
    return {
        "action": action,
        "criteria": {
            "keyword": keyword,
            "year": year,
            "month": month,
            "file_type": normalize_file_type(file_type),
            "location": location
        }
    }


def execute_command(command):
    if not command:
        return None

    action = command.get("action")
    criteria = command.get("criteria", {})

    if action == "search":
        results = src_files(criteria)
        show_results(results)
        return results
    elif action == "open":
        results = src_files(criteria)
        open_files(results)
        return results
    else:
        print("\n❌ Unknown action:", action)
        return None


def execute_commands(commands):
    all_results = []
    if not commands:
        return all_results
    for command in commands:
        results = execute_command(command)
        all_results.append({"command": command, "results": results})
    return all_results


AI_TOOLS = {
    "search_files": "Search files using keyword, year, month, type and location.",
    "search_folders": "Search folders by name.",
    "open_files": "Open one or multiple matching files.",
    "count_files": "Count all files.",
    "count_folders": "Count all folders."
}


def execute_ai_tool(tool_name, arguments):
    arguments = arguments or {}

    if tool_name == "search_files":
        criteria = build_criteria()
        set_criteria(criteria, keyword=arguments.get("keyword"), year=arguments.get("year"),
                     month=arguments.get("month"), file_type=arguments.get("file_type"),
                     location=arguments.get("location"))
        return search_file(criteria)

    elif tool_name == "search_folders":
        return search_folder(arguments.get("keyword", ""), arguments.get("location"))

    elif tool_name == "open_files":
        criteria = build_criteria()
        set_criteria(criteria, keyword=arguments.get("keyword"), year=arguments.get("year"),
                     month=arguments.get("month"), file_type=arguments.get("file_type"),
                     location=arguments.get("location"))
        results = search_file(criteria)
        open_files(results)
        return results

    elif tool_name == "count_files":
        show_file_count()
        return None

    elif tool_name == "count_folders":
        show_folder_count()
        return None

    else:
        print("\n❌ Unknown AI tool:", tool_name)
        return None


def show_results(results):
    if not results:
        print("\n❌ Not Found")
        return

    print("\n... SEARCH RESULTS ...")
    for i, result in enumerate(results, start=1):
        print("\n────────────────────")
        print(f"📄 Result {i}")
        print("────────────────────")
        print("Name:", result["name"])
        print("📍 Path:", result["path"])
        print("📁 Folder:", result["folder"])
        print("📦 Size:", result["size"], "bytes")
        print("📄 Type:", result["type"])
        print("🕐 Modified:", result["modified"])

    print("\n════════════════════")
    print("🔎 Search Complete")
    print("📁 Found:", len(results), "file(s)")
    print("════════════════════")


def show_folder_results(results):
    if not results:
        print("\n❌ Not Found")
        return

    print("\n... FOLDER RESULTS ...")
    for i, result in enumerate(results, start=1):
        print("\n────────────────────")
        print(f"📁 Result {i}")
        print("────────────────────")
        print("Name:", result["name"])
        print("📍 Path:", result["path"])

    print("\n════════════════════")
    print("📁 Found:", len(results), "folder(s)")
    print("════════════════════")


def show_file_count():
    print("Counting files...")
    for i in range(1, 6):
        print(f"\rLoading: {i * 20}%", end="", flush=True)
        time.sleep(0.2)
    print("\n")

    count = 0
    for all_folder, folders, files in os.walk("/storage/emulated/0"):
        count += len(files)
    print("Total files:", count)


def show_folder_count():
    print("Counting folders...")
    for i in range(1, 6):
        print(f"\rLoading: {i * 20}%", end="", flush=True)
        time.sleep(0.2)
    print("\n")

    count = 0
    for all_folder, folders, files in os.walk("/storage/emulated/0"):
        count += len(folders)
    print("Total folders:", count)


def show_history():
    if not history:
        print("\n📭 No search history.")
        return

    print("\n╔══════════════════════════════════════╗")
    print("║          🔎 SEARCH HISTORY           ║")
    print("╚══════════════════════════════════════╝")

    for i, item in enumerate(history, start=1):
        if not isinstance(item, dict):
            print("\n──────────────────────────────────────")
            print(f"🔹 Search #{i}")
            print("⚠️ Old/invalid history data")
            continue

        print("\n──────────────────────────────────────")
        print(f"🔹 Search #{i}")
        print("──────────────────────────────────────")
        print(f"🔤 Keyword   : {item.get('keyword') or 'Any'}")
        print(f"📅 Year      : {item.get('year') or 'Any'}")
        print(f"📆 Month     : {item.get('month') or 'Any'}")
        print(f"📄 File Type : {item.get('file_type') or 'Any'}")
        print(f"📁 Location  : {item.get('location') or 'All Storage'}")

    print("\n══════════════════════════════════════")
    print(f"📊 Total Searches: {len(history)}")
    print("══════════════════════════════════════")


def manual_search():
    criteria = reset_criteria()

    print("\n========== FILE SEARCH ==========")
    print("Leave blank if you don't want to use a filter.\n")

    keyword = input("Keyword (file name): ").strip() or None
    year = get_integer("Year (example: 2025): ")
    month = get_integer("Month (1-12): ")
    file_type = input("File type (pdf/txt/docx): ").strip() or None
    location = input("Location (blank = all storage): ").strip() or None

    set_criteria(criteria, keyword=keyword, year=year, month=month,
                 file_type=file_type, location=location)

    print("\nSearching...")
    results = search_file(criteria)

    add_history({
        "keyword": keyword,
        "year": year,
        "month": month,
        "file_type": normalize_file_type(file_type),
        "location": location
    })

    return results


def menu():
    print("""
==============================
       SMART FILE SCANNER
==============================

1. Search File
2. Search Folder
3. Show File Count
4. Show Folder Count
5. Search History
6. Multiple Search
7. Exit

==============================
""")


def main():
    menu()

    while True:
        choice = input("Choice: ").strip()

        if choice == "1":
            clear()
            results = manual_search()
            clear()
            show_results(results)
            input("\nPress Enter to continue...")
            clear()
            menu()

        elif choice == "2":
            clear()
            search = input("Search Folder: ").strip()
            clear()
            results = search_folder(search)
            show_folder_results(results)
            input("\nPress Enter to continue...")
            clear()
            menu()

        elif choice == "3":
            clear()
            show_file_count()
            input("\nPress Enter to continue...")
            clear()
            menu()

        elif choice == "4":
            clear()
            show_folder_count()
            input("\nPress Enter to continue...")
            clear()
            menu()

        elif choice == "5":
            clear()
            show_history()
            input("\nPress Enter to continue...")
            clear()
            menu()

        elif choice == "6":
            clear()
            criteria_list = multiple_search()
            if criteria_list:
                all_results = search_multiple(criteria_list)
                clear()
                show_multiple_results(all_results)
            input("\nPress Enter to continue...")
            clear()
            menu()

        elif choice == "7":
            clear()
            print("Exit...")
            break

        else:
            print("❌ Invalid choice")


if __name__ == "__main__":
    main()
#ja ja use hoyse code e 
#os module:
#os.system()
#os.name
#os.path.exists()
#os.path.join()
#os.path.getsize()
#os.path.getmtime()
#os.path.splitext()
#os.walk()
#os.startfile()
#time module:
#time.localtime()
#time.ctime()
#time.sleep()
#.tm_year
#.tm_mon
#json module:
#json.dump()
#json.load()
#Python built-in functions:
#open()
#input()
#print()
#int()
#str()
#len()
#range()
#enumerate()
#isinstance()
#String methods:
#.lower()
#.strip()
#.lstrip()
#Dict methods:
#.get()
#List methods:
#.append()
#.pop()