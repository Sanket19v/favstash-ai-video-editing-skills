import json

with open("video-engine/aligned_captions.json", "r", encoding="utf-8") as f:
    aligned = json.load(f)

turn_ranges = aligned["turn_ranges"]
total_seconds = int(aligned["total_duration"]) # 93 seconds

with open("audio/delivery_opt_turns/turns_metadata.json", "r", encoding="utf-8") as f:
    raw_turns = json.load(f)

# Every second has a UNIQUE graphic ID, title, breadcrumb, and stepNumber
# Directly tied to what the speaker is saying at that exact second!
SCENE_SPECS = {
    # Turn 0: Peter: "Can Windows really use my computer without permission?" [0.0 - 2.74]
    0: ("sec00_desktop_start", "Is Windows Using Your PC?", "Windows 11 Background Activity", 0),
    1: ("sec01_unauthorized_access", "Without Your Permission?", "Background Network Requests", 0),
    2: ("sec02_permission_bypassed", "Permission Bypassed!", "Default Windows Privileges", 0),

    # Turn 1: Stewie: "It already is. You've been seeding Windows updates to strangers since the day you installed it." [2.74 - 7.40]
    3: ("sec03_status_seeder_active", "It Already Is Active", "Status: Active Seeder Node", 0),
    4: ("sec04_seeding_updates", "Seeding Windows Updates", "Uploading Cached Files", 0),
    5: ("sec05_strangers_connecting", "Uploading To Strangers", "14 Stranger IP Connections", 0),
    6: ("sec06_since_install_day", "Active Since First PC Boot", "Day 1 Default Setting", 0),

    # Turn 2: Peter: "So everyone's computer is doing this?" [7.40 - 9.10]
    7: ("sec07_everyones_pc", "Everyone's Computer?", "Millions of Connected PCs", 0),
    8: ("sec08_global_swarm_mesh", "1.4 Billion Windows PCs", "Global Peer-to-Peer Mesh", 0),

    # Turn 3: Stewie: "Every Windows 10 and 11 PC is secretly part of Microsoft's free CDN network, and one toggle in Settings turns it all off." [9.10 - 16.08]
    9: ("sec09_win10_affected", "Windows 10 Affected", "Pre-Enabled Out-of-the-Box", 0),
    10: ("sec10_win11_affected", "Windows 11 Affected", "Enabled By Default", 0),
    11: ("sec11_secret_cdn_part", "Secret CDN Network", "User PCs Acting As Servers", 0),
    12: ("sec12_free_cdn_savings", "Microsoft's Free CDN", "Offloading Cloud Infrastructure", 0),
    13: ("sec13_you_are_server", "Your PC Is Their Server", "Free Bandwidth Donation", 0),
    14: ("sec14_one_toggle_preview", "One Toggle In Settings", "Windows Update Settings", 0),
    15: ("sec15_turns_it_off_teaser", "Turns It All Off", "One Switch Halts All Seeding", 0),

    # Turn 4: Peter: "Wait, like BitTorrent seeding?" [16.08 - 17.78]
    16: ("sec16_bittorrent_logo", "Like BitTorrent Seeding?", "P2P Protocol Comparison", 0),
    17: ("sec17_bittorrent_swarm", "Yes, BitTorrent Protocol", "Swarm Distribution Logic", 0),

    # Turn 5: Stewie: "Exactly. But Microsoft never told you this was turned on by default." [17.78 - 21.56]
    18: ("sec18_exactly_confirmed", "Exactly That Technology", "Peer-To-Peer File Swarms", 0),
    19: ("sec19_never_told_you", "Microsoft Never Told You", "Zero Notifications Given", 0),
    20: ("sec20_turned_on_default", "Turned ON by Default", "Hidden During PC Setup", 0),

    # Turn 6: Peter: "How much bandwidth are we talking?" [21.56 - 23.10]
    21: ("sec21_measuring_bandwidth", "How Much Bandwidth?", "Testing Network Drain", 0),
    22: ("sec22_gauge_climbing", "Testing Upload Drain", "Speedometer Rising Rapidly", 0),

    # Turn 7: Stewie: "Therefore, some users report 80% of their upload speed getting consumed, which is why your Zoom calls freeze." [23.10 - 29.36]
    23: ("sec23_user_reports", "User Speed Reports", "Community Forum Findings", 0),
    24: ("sec24_big_80_percent", "80% Upload Consumed!", "Heavy Network Saturation", 0),
    25: ("sec25_upload_bar_red", "Upload Speed Choked", "80% Used by Windows", 0),
    26: ("sec26_choked_pipe", "Internet Pipe Saturated", "Only 20% Bandwidth Left", 0),
    27: ("sec27_ping_spiking", "Latency Spike: 280ms Ping", "High Packet Loss Detected", 0),
    28: ("sec28_zoom_freeze_alert", "Why Your Zoom Calls Freeze", "Video Buffering & Audio Drop", 0),

    # Turn 8: Peter: "That seems illegal." [29.36 - 30.42]
    29: ("sec29_seems_illegal", "That Seems Illegal!", "Consumer Rights Question", 0),

    # Turn 9: Stewie: "It's buried in the terms you didn't read. But here's what's worse: Task Manager hides it as Service Host, Network Service. So you can't even see what's happening." [30.42 - 38.68]
    30: ("sec30_buried_in_terms", "Buried In User Terms", "Microsoft Service Agreement", 0),
    31: ("sec31_terms_fine_print", "Page 42 Fine Print", "The Clause Nobody Reads", 0),
    32: ("sec32_heres_whats_worse", "Here Is What's Worse...", "The Task Manager Disguise", 0),
    33: ("sec33_taskmgr_ctrl_shift_esc", "Ctrl + Shift + Esc", "Opening Windows Task Manager", 0),
    34: ("sec34_taskmgr_scrolling", "Task Manager Processes", "Looking For The Culprit", 0),
    35: ("sec35_service_host_highlight", "Service Host: Network Service", "Generic Process Name", 0),
    36: ("sec36_svchost_85mbps", "Eating 85.4 Mbps Upload!", "Hidden Under svchost.exe", 0),
    37: ("sec37_cant_even_see", "You Can't Even See It", "Generic Label Conceals P2P", 0),
    38: ("sec38_mask_peeled_back", "The Mask Revealed", "svchost = Delivery Optimization", 0),

    # Turn 10: Peter: "Right. You just see mystery processes eating bandwidth." [38.68 - 42.06]
    39: ("sec39_mystery_processes", "Mystery Processes", "Unknown Background Traffic", 0),
    40: ("sec40_eating_bandwidth", "Eating Your Bandwidth", "Background Bandwidth Vampire", 0),
    41: ("sec41_user_frustration", "Ghost Traffic Everywhere", "Unaccounted Upload Spikes", 0),

    # Turn 11: Stewie: "Therefore, most people blame their ISP instead of Windows." [42.06 - 45.28]
    42: ("sec42_people_blame_isp", "Most Blame Their ISP", "Assuming Bad Internet Provider", 0),
    43: ("sec43_router_innocent", "Your Router Is Innocent!", "Hardware Is Working Normally", 0),
    44: ("sec44_windows_is_culprit", "Windows Is The Culprit", "The Leak Is Inside Windows", 0),

    # Turn 12: Peter: "Why would Microsoft do this?" [45.28 - 46.98]
    45: ("sec45_why_microsoft_cloud", "Why Does Microsoft Do This?", "The Financial Incentive", 0),
    46: ("sec46_money_savings_icon", "Massive Server Savings", "Cutting Datacenter Costs", 0),

    # Turn 13: Stewie: "They deliver 3.5 billion updates monthly. Peer-to-peer means they offload server costs to your electricity bill and internet plan." [46.98 - 55.16]
    47: ("sec47_stat_3_5_billion_intro", "3.5 Billion Updates", "Staggering Distribution Volume", 0),
    48: ("sec48_stat_3_5_billion_boxes", "Monthly Distribution Load", "Billions of Gigabytes", 0),
    49: ("sec49_p2p_mesh_flow", "Peer-To-Peer Flow", "Users Seeding Each Other", 0),
    50: ("sec50_offload_server_costs", "Offloading Server Costs", "Cloud Bandwidth Cost: $0", 0),
    51: ("sec51_servers_shut_down", "Saving Azure Infrastructure", "Passing The Load To You", 0),
    52: ("sec52_electricity_spinning", "Your Electricity Meter Spins", "PC Fans & Hardware Strained", 0),
    53: ("sec53_electricity_bill_up", "On Your Power Bill", "Higher Home Energy Usage", 0),
    54: ("sec54_internet_plan_cap", "And Your Internet Plan!", "Eating Monthly Data Caps", 0),

    # Turn 14: Peter: "Do they at least limit it to your local network?" [55.16 - 57.42]
    55: ("sec55_home_wifi_lan", "Limit To Local Network?", "Peter's Reasonable Question", 0),
    56: ("sec56_local_devices_only", "Just Devices In My Home?", "Sharing Between 2 Laptops", 0),

    # Turn 15: Stewie: "That's the misdirection. There's a setting for PCs on my local network. But the default includes PCs on the internet." [57.42 - 63.68]
    57: ("sec57_the_misdirection", "That's The Misdirection!", "A Clever UI Illusion", 0),
    58: ("sec58_two_radio_buttons", "Two Options In Settings", "Local LAN vs Entire World", 0),
    59: ("sec59_radio_local_safe", "Option 1: Local Network", "Safe: Only Your Other Home PCs", 0),
    60: ("sec60_radio_internet_default", "Option 2: The Internet", "Pre-Checked By Microsoft!", 0),
    61: ("sec61_default_includes_strangers", "Default Includes The World", "Wide Open Internet Seeding", 0),
    62: ("sec62_worldwide_swarms", "Connected To Strangers", "Global Upload Stream Active", 0),

    # Turn 16: Peter: "You're uploading to random strangers worldwide." [63.68 - 66.34]
    63: ("sec63_strangers_avatars", "Random Strangers Worldwide!", "Unknown IP Addresses", 0),
    64: ("sec64_uploading_across_globe", "Sending Your Data Out", "Bandwidth Sent Overseas", 0),
    65: ("sec65_unencrypted_swarm", "Global Seeding Swarm", "Your PC Is An Active Node", 0),

    # Turn 17: Stewie: "Yep. Your gaming laptop in Ohio might be seeding updates to someone in Germany right now." [66.34 - 71.16]
    66: ("sec66_yep_confirmed", "Yep, Exactly What Happens", "Real-World Example", 0),
    67: ("sec67_gaming_laptop_ohio", "Gaming Laptop in Ohio", "Columbus, Ohio • 300W Rig", 0),
    68: ("sec68_atlantic_data_beam", "Crossing The Atlantic", "Transmitting Windows CABs", 0),
    69: ("sec69_stranger_germany", "Stranger In Germany", "Berlin Peer Downloading", 0),
    70: ("sec70_stranger_download_done", "Downloading From Your PC!", "Using Your Electricity & ISP", 0),

    # Turn 18: Peter: "How do I stop this immediately?" [71.16 - 72.78]
    71: ("sec71_how_to_stop_emergency", "How Do I Stop This?", "Emergency Solution Needed", 0),
    72: ("sec72_5_clicks_teaser", "Follow These 5 Clicks", "Permanent Windows Fix", 0),

    # Turn 19: Stewie: "Open Windows Settings. Go to Windows Update. Click Advanced Options. Then Delivery Optimization. Toggle Allow Downloads from Other PCs to Off." [72.78 - 81.20]
    73: ("sec73_click1_open_settings", "Click 1: Open Settings", "Press Windows Key + I", 1),
    74: ("sec74_click2_windows_update", "Click 2: Windows Update", "Click On Windows Update Tab", 1),
    75: ("sec75_click3_advanced_options", "Click 3: Advanced Options", "Scroll To Additional Options", 1),
    76: ("sec76_click4_delivery_opt", "Click 4: Delivery Optimization", "Select Delivery Optimization", 1),
    77: ("sec77_finding_the_switch", "Found: Allow Downloads", "Currently Turned ON (Blue)", 1),
    78: ("sec78_cursor_approaching_switch", "Prepare To Toggle Off", "Moving Cursor To The Switch", 1),
    79: ("sec79_click5_toggle_off", "Click 5: Toggle Switch OFF", "Click To Disable Seeding", 1),
    80: ("sec80_switch_turned_grey_off", "Switch Turned OFF!", "Grey Switch = Disabled", 1),

    # Turn 20: Peter: "That's it?" [81.20 - 81.70]
    81: ("sec81_thats_it_question", "That's It?!", "Done In Just 30 Seconds", 0),

    # Turn 21: Stewie: "That's it. Five clicks and you're no longer Microsoft's free bandwidth." [81.70 - 85.24]
    82: ("sec82_five_clicks_checklist", "Five Clicks Complete!", "Settings › Update › Adv › Opt › Off", 0),
    83: ("sec83_no_longer_free_bandwidth", "No Longer Free Bandwidth", "Connection Severed Forever", 0),
    84: ("sec84_bandwidth_liberated", "Bandwidth 100% Liberated", "0 kbps Unwanted Upload", 0),

    # Turn 22: Peter: "So Task Manager lies, and now Windows steals bandwidth." [85.24 - 88.94]
    85: ("sec85_taskmgr_lies_question", "Task Manager Lies?", "Mystery Process Revealed", 0),
    86: ("sec86_windows_steals_bandwidth", "Windows Steals Bandwidth", "Background Leaks Stopped", 0),
    87: ("sec87_taskmgr_clean_0mbps", "Task Manager: 0 Mbps Upload", "Network Traffic Clean & Idle", 0),
    88: ("sec88_speedtest_100_percent", "100% Upload Restored!", "Zero Background Drain", 0),

    # Turn 23: Stewie: "Task Manager doesn't lie. It just shows you what Microsoft wants you to see." [88.94 - 93.04]
    89: ("sec89_taskmgr_truth_lens", "Task Manager Doesn't Lie", "It Shows What OS Allows", 0),
    90: ("sec90_zoom_smooth_hd", "Zoom Calls 100% Crystal Clear", "Smooth 60 FPS • Zero Lag", 0),
    91: ("sec91_master_pc_tips_card", "PC Tips by Ez_peter", "Take Back Control Of Your PC", 0),
    92: ("sec92_follow_ez_peter_cta", "Follow @Ez_peter", "Save & Share This PC Tip!", 0)
}

script_items = []
for s in range(total_seconds):
    t_center = s + 0.5
    active_turn = turn_ranges[-1]
    for tr in turn_ranges:
        if tr["start"] <= t_center < tr["end"]:
            active_turn = tr
            break
            
    t_idx = active_turn["line_index"]
    spk = active_turn["speaker"]
    full_sentence = raw_turns[t_idx]["text"]
    
    graphic, title, breadcrumb, step_num = SCENE_SPECS[s]
    
    script_items.append({
        "second": s,
        "speaker": spk,
        "line": full_sentence,
        "graphic": graphic,
        "stepNumber": step_num,
        "title": title,
        "breadcrumb": breadcrumb
    })

print(f"Generated {len(script_items)} distinct script items.")
with open("script.json", "w", encoding="utf-8") as f:
    json.dump(script_items, f, indent=2)

with open("output/script.json", "w", encoding="utf-8") as f:
    json.dump(script_items, f, indent=2)

print("Saved script.json and output/script.json successfully!")
