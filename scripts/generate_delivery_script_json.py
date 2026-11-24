import json

with open("video-engine/aligned_captions.json", "r", encoding="utf-8") as f:
    aligned = json.load(f)

turn_ranges = aligned["turn_ranges"]
total_seconds = int(aligned["total_duration"]) # 93 seconds

with open("audio/delivery_opt_turns/turns_metadata.json", "r", encoding="utf-8") as f:
    raw_turns = json.load(f)

# Define exact second-by-second scenes matching the dialogue
scenes = {
    0: ("win_desktop_normal", "Is Windows Using Your PC?", "Windows 11 Background Activity", 0),
    1: ("win_network_spike", "Secret Background Activity", "Unexplained Network Spike", 0),
    2: ("warning_bandwidth_alert", "Hidden Seeder Active", "Bandwidth Leaving Your PC", 0),
    3: ("p2p_seeding_strangers", "Seeding Windows Updates", "Active Since First PC Boot", 0),
    4: ("p2p_network_mesh", "Uploading to Strangers", "Peer-to-Peer File Distribution", 0),
    5: ("cdn_cloud_offload", "Microsoft CDN Network", "Your PC As A Cloud Node", 0),
    6: ("p2p_seeding_counter", "14 Active Stranger Peers", "Seeding Windows Update Chunks", 0),
    7: ("global_pcs_map", "Every Windows 10 & 11 PC", "Billions of Connected Devices", 0),
    8: ("global_pcs_mesh", "Secret Global CDN", "Built Directly Into Windows", 0),
    9: ("bittorrent_comparison", "Just Like BitTorrent Seeding", "P2P Swarm File Sharing", 0),
    10: ("bittorrent_swarm", "Your PC Is A Seeder", "Constant Background Uploading", 0),
    11: ("secret_default_badge", "Turned ON by Default", "Zero User Notification", 0),
    12: ("secret_terms_doc", "Microsoft Never Told You", "Default Windows 11 Config", 0),
    13: ("settings_toggle_preview", "One Hidden Toggle", "Windows Settings › Update", 0),
    14: ("network_toggle_badge", "Stops All Seeding", "Takes 5 Clicks To Turn Off", 0),
    15: ("bandwidth_question", "How Much Bandwidth?", "Measuring The Hidden Drain", 0),
    16: ("upload_gauge_80", "Up to 80% Upload Speed", "Consuming Your Network Cap", 0),
    17: ("upload_spike_graph", "80% Upload Saturated", "Leaving 20% For Your Apps", 0),
    18: ("zoom_freeze_warning", "Why Your Zoom Calls Freeze", "Audio Drops & Video Stutter", 0),
    19: ("gaming_lag_alert", "High Latency & Lag Spikes", "280ms Ping In Online Games", 0),
    20: ("zoom_lag_details", "Packet Loss Detected", "Caused By Background Seeding", 0),
    21: ("terms_service_modal", "Buried In User Terms", "Microsoft Services Agreement", 0),
    22: ("terms_small_print", "The Clause Nobody Reads", "Delivery Optimization Section", 0),
    23: ("task_manager_opening", "Open Task Manager", "Ctrl + Shift + Esc", 0),
    24: ("task_manager_disguise", "Hidden Under Generic Name", "Concealed From Users", 0),
    25: ("task_manager_svchost", "Service Host: Network Service", "svchost.exe (Delivery Opt)", 0),
    26: ("task_manager_bandwidth", "Eating 85 Mbps Upload", "Disguised System Process", 0),
    27: ("isp_blame_modal", "Most People Blame Their ISP", "Assuming Internet Provider Fault", 0),
    28: ("isp_router_normal", "Your Router Is Innocent", "Windows Is Eating The Bandwidth", 0),
    29: ("why_microsoft_title", "Why Does Microsoft Do It?", "The Multi-Million Dollar Reason", 0),
    30: ("stat_3_5_billion", "3.5 Billion Updates Monthly", "Huge Distribution Scale", 0),
    31: ("stat_server_costs", "Saving Millions In Servers", "Cutting Cloud Infrastructure", 0),
    32: ("electricity_bill_card", "On Your Electricity Bill", "Your Hardware Powers It", 0),
    33: ("internet_plan_cap", "Eating Your Internet Plan", "ISP Monthly Data Limits", 0),
    34: ("datacenter_vs_user", "Offloading Cloud Costs", "From Azure To Your Living Room", 0),
    35: ("local_network_question", "Only On Local Network?", "Peter's Reasonable Question", 0),
    36: ("local_vs_internet_toggle", "The Setting's Misdirection", "Local Network vs Internet", 0),
    37: ("default_radio_internet", "Default: Internet PCs", "Worldwide Seeding Active", 0),
    38: ("strangers_worldwide_map", "Uploading To Strangers", "Global Distribution Swarm", 0),
    39: ("ohio_to_germany_map", "Ohio PC → Germany Seeder", "Cross-Continental Seeding", 0),
    40: ("gaming_laptop_uploading", "Gaming Rig in Ohio", "Uploading Windows CAB Files", 0),
    41: ("berlin_peer_receiving", "Stranger In Germany", "Downloading From Your PC", 0),
    42: ("stop_it_immediately", "How To Stop This Now", "Turn Off Seeding In 5 Clicks", 0),
    43: ("stop_overview_card", "5-Click Solution Guide", "Take 30 Seconds To Fix", 0),
    44: ("settings_icon_pop", "Windows Settings App", "Ready To Configure", 0),
    45: ("cdn_switch_ready", "Delivery Optimization", "The Setting Microsoft Hid", 0),
    46: ("bandwidth_lock_free", "Prepare To Toggle Off", "Reclaim Your Upload Speed", 0),
    47: ("step_intro_graphic", "Step-By-Step Walkthrough", "Follow Along On Your PC", 1),
    48: ("step_intro_keycap", "Press Windows Key + I", "Quick Shortcut To Settings", 1),
    49: ("step_intro_update", "Click Windows Update", "Bottom Left Navigation Tab", 1),
    50: ("step_intro_advanced", "Select Advanced Options", "Scroll To Additional Settings", 1),
    51: ("step_intro_delivery", "Click Delivery Optimization", "Peer-To-Peer Control Panel", 1),
    52: ("step_intro_switch", "Allow Downloads: Set OFF", "Disable Free Seeding", 1),
    53: ("bandwidth_recap_badge", "Instant Upload Recovery", "100% Bandwidth Back", 0),
    54: ("zoom_restored_badge", "Zoom Calls Back To Normal", "Zero Packet Loss", 0),
    55: ("local_lan_diagram", "Local Network Option", "Keep Local LAN Only If Desired", 0),
    56: ("local_lan_details", "PCs On My Local Network", "Safe Alternative", 0),
    57: ("internet_toggle_risk", "Internet Seeding Risk", "Why Internet Default Is Bad", 0),
    58: ("radio_internet_selected", "Default: PCs on the Internet", "Pre-Checked By Microsoft", 0),
    59: ("misdirection_badge", "The Clever Misdirection", "Hidden Under Vague Labels", 0),
    60: ("bandwidth_leak_card", "The Bandwidth Leak", "Now Fully Understood", 0),
    61: ("global_seeder_stop", "Global Seeding Stopped", "Cutting Off Stranger Swarms", 0),
    62: ("ohio_laptop_safe", "Ohio Gaming PC Safe", "No More German Downloads", 0),
    63: ("germany_disconnected", "Remote Peer Disconnected", "Your Upload Is Saved", 0),
    64: ("how_to_fix_title", "Fix It In 5 Clicks", "Step-By-Step Solution", 1),
    65: ("settings_action_open", "Click 1: Open Settings", "Press Windows Key + I", 1),
    66: ("settings_action_update", "Click 2: Windows Update", "Click On Windows Update Tab", 1),
    67: ("settings_action_advanced", "Click 3: Advanced Options", "Click Advanced Options Menu", 1),
    68: ("settings_action_delivery", "Click 4: Delivery Optimization", "Select Delivery Optimization", 1),
    69: ("settings_action_found", "Setting Located", "Allow Downloads From Other PCs", 1),
    70: ("settings_toggle_switch_on", "Notice It Is Turned ON", "Blue Switch Indicates Active", 1),
    71: ("settings_cursor_approach", "Moving Cursor To Switch", "Preparing To Toggle Off", 1),
    72: ("settings_toggle_click", "Click 5: Toggle Switch OFF", "Click Switch To Disable", 1),
    73: ("settings_toggle_switch_off", "Switch Turned OFF", "Grey Switch Indicates Disabled", 1),
    74: ("solution_confirmed_badge", "Seeding Deactivated", "Microsoft CDN Disconnected", 1),
    75: ("five_clicks_complete", "Five Clicks Complete", "Settings › Update › Advanced › Opt", 1),
    76: ("bandwidth_freed_card", "Bandwidth Fully Liberated", "0 kbps Unwanted Upload", 0),
    77: ("no_longer_free_cdn", "No Longer Microsoft's Free CDN", "Your PC Is Yours Again", 0),
    78: ("speed_restored_gauge", "Upload Speeds Restored", "100% Capacity Available", 0),
    79: ("zoom_lag_cured", "Crystal Clear Zoom Calls", "Smooth 60fps Video & Audio", 0),
    80: ("ping_drops_card", "Ping Drops From 280ms to 18ms", "Lag-Free Online Gaming", 0),
    81: ("thats_it_confirm", "That's It! Completely Done", "Permanent System Setting", 0),
    82: ("free_bandwidth_ended", "No Longer Free Bandwidth", "Saved Bandwidth & Electricity", 0),
    83: ("five_clicks_victory", "5 Clicks • 30 Seconds", "Quickest Windows Optimization", 0),
    84: ("taskmgr_truth_card", "The Truth About Task Manager", "Why It Hides The Truth", 0),
    85: ("svchost_exposed", "svchost.exe Exposed", "Service Host Traffic Cleared", 0),
    86: ("windows_steals_bandwidth", "Windows Hidden Costs", "Now Under Your Control", 0),
    87: ("taskmgr_clean_state", "Task Manager: 0% Network", "Completely Idle & Clean", 0),
    88: ("microsoft_filter_reveal", "What Microsoft Shows You", "Peeling Back The Defaults", 0),
    89: ("mastery_summary_badge", "Windows Master Optimization", "One Of Many Hidden Settings", 0),
    90: ("recap_action_card", "Share With PC Owners", "Help Friends Fix Their Lag", 0),
    91: ("ez_peter_branding_card", "PC Tips by Ez_peter", "Follow For Daily Windows Tips", 0),
    92: ("follow_ez_peter_cta", "Follow @Ez_peter", "Save This Reel For Later!", 0)
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
    
    scene_info = scenes.get(s, ("win_desktop_normal", "PC Tips by Ez_peter", "Windows Optimization", 0))
    graphic, title, breadcrumb, step_num = scene_info
    
    script_items.append({
        "second": s,
        "speaker": spk,
        "line": full_sentence,
        "graphic": graphic,
        "stepNumber": step_num,
        "title": title,
        "breadcrumb": breadcrumb
    })

print(f"Generated {len(script_items)} script items.")

with open("script.json", "w", encoding="utf-8") as f:
    json.dump(script_items, f, indent=2)

with open("output/script.json", "w", encoding="utf-8") as f:
    json.dump(script_items, f, indent=2)

print("Saved script.json and output/script.json!")
