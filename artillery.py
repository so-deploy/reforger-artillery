import os
import math

# ==========================================
# BALLISTICS DATA TABLES (Range, Elev, ToF, dElev)
# ==========================================

GRAD_DATA = [
    (200, 19, 1.0, 110), (400, 23, 1.5, 108), (600, 29, 2.1, 102), (800, 35, 2.6, 91), (1000, 42, 3.1, 80),
    (1200, 48, 3.6, 70), (1400, 55, 4.2, 61), (1600, 62, 4.8, 54), (1800, 68, 5.3, 49), (2000, 75, 5.9, 45),
    (2200, 82, 6.4, 42), (2400, 89, 7.0, 39), (2600, 97, 7.6, 37), (2800, 104, 8.1, 35), (3000, 111, 8.7, 33),
    (3200, 119, 9.3, 31), (3400, 127, 9.9, 30), (3600, 134, 10.5, 28), (3800, 142, 11.1, 27), (4000, 150, 11.7, 26),
    (4200, 158, 12.4, 25), (4400, 166, 13.0, 25), (4600, 175, 13.6, 24), (4800, 183, 14.2, 23), (5000, 192, 14.9, 23),
    (5200, 200, 15.6, 22), (5400, 209, 16.2, 22), (5600, 218, 17.0, 22), (5800, 228, 17.6, 22)
]

HOWITZER_DATA = {
    1: [(950, 1245, 24.4, 24), (1000, 1221, 24.2, 24), (1050, 1197, 24.0, 26), (1100, 1171, 23.7, 27), (1150, 1144, 23.4, 29), (1200, 1115, 23.1, 31), (1250, 1084, 22.7, 34), (1300, 1050, 22.3, 39), (1350, 1011, 21.8, 46), (1400, 965, 21.2, 58), (1450, 907, 20.3, 107), (1500, 800, 18.6, 0)],
    2: [(1500, 1270, 33.1, 13), (1550, 1257, 33.0, 14), (1600, 1243, 32.9, 14), (1650, 1229, 32.7, 15), (1700, 1214, 32.5, 14), (1750, 1200, 32.4, 15), (1800, 1185, 32.1, 16), (1850, 1169, 31.9, 16), (1900, 1153, 31.7, 17), (1950, 1136, 31.5, 17), (2000, 1119, 31.2, 18), (2050, 1101, 31.0, 19), (2100, 1082, 30.7, 20), (2150, 1062, 30.3, 21), (2200, 1041, 30.0, 23), (2250, 1018, 29.6, 23), (2300, 995, 29.2, 28), (2350, 967, 28.7, 29), (2400, 938, 28.1, 34), (2450, 904, 27.5, 44), (2500, 860, 26.5, 0)],
    3: [(2100, 1272, 41.0, 10), (2200, 1253, 40.8, 10), (2300, 1233, 40.5, 10), (2400, 1213, 40.2, 11), (2500, 1192, 39.9, 11), (2600, 1170, 39.5, 12), (2700, 1147, 39.1, 12), (2800, 1123, 38.7, 13), (2900, 1098, 38.3, 14), (3000, 1070, 37.7, 14), (3100, 1042, 37.2, 16), (3200, 1010, 36.5, 16), (3300, 975, 35.7, 18), (3400, 936, 34.9, 22), (3500, 890, 33.7, 28), (3600, 828, 32.1, 0)],
    4: [(2600, 1271, 47.2, 8), (2700, 1255, 47.0, 7), (2800, 1240, 46.7, 8), (2900, 1224, 46.5, 9), (3000, 1207, 46.2, 9), (3100, 1190, 45.9, 9), (3200, 1172, 45.6, 9), (3300, 1154, 45.2, 9), (3400, 1135, 44.9, 9), (3500, 1116, 44.5, 10), (3600, 1095, 44.0, 10), (3700, 1074, 43.6, 11), (3800, 1052, 43.1, 12), (3900, 1028, 42.5, 12), (4000, 1003, 41.9, 14), (4100, 976, 41.3, 15), (4200, 946, 40.5, 17), (4300, 912, 39.6, 17), (4400, 874, 38.5, 20), (4500, 828, 37.2, 26)],
    5: [(3000, 1271, 52.2, 7), (3100, 1258, 52.0, 7), (3200, 1244, 51.8, 7), (3300, 1230, 51.5, 7), (3400, 1216, 51.3, 7), (3500, 1202, 51.0, 7), (3600, 1187, 50.7, 7), (3700, 1172, 50.4, 8), (3800, 1156, 50.1, 7), (3900, 1140, 49.8, 8), (4000, 1124, 49.4, 9), (4100, 1107, 49.0, 9), (4200, 1089, 48.6, 9), (4300, 1071, 48.2, 9), (4400, 1052, 47.7, 10), (4500, 1032, 47.2, 10), (4600, 1011, 46.7, 10), (4700, 989, 46.1, 11), (4800, 966, 45.5, 12), (4900, 941, 44.7, 13), (5000, 913, 44.0, 14), (5100, 883, 43.1, 16), (5200, 850, 42.0, 20), (5300, 809, 40.7, 0)]
}

# ==========================================
# PARSING & CALCULATIONS
# ==========================================

def parse_coordinates(input_str):
    parts = input_str.strip().split()
    if len(parts) < 3:
        raise ValueError("Input X, Y, and Z (Elevation).")

    raw_x_str = parts[0]
    raw_y_str = parts[1]
    raw_z_str = parts[2]

    # Use raw meters if input is 4+ digits, else grid * 100
    is_raw = len(raw_x_str) >= 4
    base_x = float(raw_x_str) if is_raw else float(raw_x_str) * 100.0
    base_y = float(raw_y_str) if is_raw else float(raw_y_str) * 100.0
    base_z = float(raw_z_str)
    
    numpad_str = ""
    name_idx = 3
    if len(parts) > 3 and parts[3].isdigit() and all(c in "123456789" for c in parts[3]):
        numpad_str = parts[3]
        name_idx = 4

    name = " ".join(parts[name_idx:]) if len(parts) > name_idx else "Target"

    # Infinite Numpad Logic
    size = 100.0 if not is_raw else 10.0
    x, y = base_x, base_y
    numpad_map = {'7':(0,2), '8':(1,2), '9':(2,2), '4':(0,1), '5':(1,1), '6':(2,1), '1':(0,0), '2':(1,0), '3':(2,0)}

    if numpad_str:
        for char in numpad_str:
            size /= 3.0
            col, row = numpad_map[char]
            x += col * size
            y += row * size
        # If numpads were used, snap to center of the smallest resolved box
        x += (size / 2.0)
        y += (size / 2.0)
    else:
        # No numpads: If it's a 3-digit grid, center it. If it's raw 4+ digits, leave exactly as is.
        if not is_raw:
            x += 50.0
            y += 50.0

    return x, y, base_z, name

def interpolate(dist, table):
    if dist < table[0][0] or dist > table[-1][0]: return None
    for i in range(len(table) - 1):
        r1, e1, t1, de1 = table[i]
        r2, e2, t2, de2 = table[i+1]
        if r1 <= dist <= r2:
            if r1 == r2: return e1, t1, de1
            ratio = (dist - r1) / (r2 - r1)
            e = e1 + ratio * (e2 - e1)
            t = t1 + ratio * (t2 - t1)
            de = de1 + ratio * (de2 - de1)
            return e, round(t, 1), de
    return None

# ==========================================
# MAIN INTERFACE
# ==========================================

def main():
    weapon, pos_x, pos_y, pos_z, targets = None, None, None, None, []
    state = "WEAPON"

    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        print("[-] Select Weapon | [=] My Position | [CTRL+C] Exit\n" + "="*50)

        if state == "WEAPON":
            print("Select: [1] Grad | [2] Howitzer")
            choice = input("> ").strip()
            if choice in ['1', '2']:
                weapon = "grad" if choice == '1' else "howitzer"
                state = "POSITION"
            continue

        if state == "POSITION":
            print(f"WEAPON: {weapon.upper()}")
            val = input("Enter Your Position (X Y Z [Numpad]): ").strip()
            if val == '-': state = "WEAPON"; continue
            try:
                pos_x, pos_y, pos_z, _ = parse_coordinates(val)
                targets = []
                state = "TARGETS"
            except: continue
            continue

        if state == "TARGETS":
            print(f"FIRE FROM: X:{pos_x:.1f} Y:{pos_y:.1f} Z:{pos_z:.1f} | WEAPON: {weapon.upper()}\n")
            
            for t in targets:
                print(f"{t['label']} ({t['dist']}m | {t['coord_str']})")
                print(f"{t['output']}\n")

            val = input("Next Target (X Y Z [Numpad]): ").strip()
            if val == '-': state = "WEAPON"; continue
            if val == '=': state = "POSITION"; continue
            if not val: continue
            
            try:
                tx, ty, tz, tname = parse_coordinates(val)
                dx, dy = tx - pos_x, ty - pos_y
                dist = math.sqrt(dx**2 + dy**2)
                dz = tz - pos_z
                
                az_mil = int(round(((math.degrees(math.atan2(dx, dy)) + 360) % 360) * (6400/360)))
                
                results = []
                if weapon == "grad":
                    sol = interpolate(dist, GRAD_DATA)
                    if sol:
                        base_e, tof, delev = sol
                        # Grad fires Low Arc (Elevation increases to shoot further)
                        # Higher target -> Needs to shoot further horizontally -> Add elevation
                        adj_e = int(round(base_e + (dz / 100.0) * delev))
                        results.append(f"↔ {az_mil} mil / ↕ {adj_e} mil ({tof}s)")
                    else:
                        results.append("OUT OF RANGE")
                else:
                    for c, tbl in HOWITZER_DATA.items():
                        sol = interpolate(dist, tbl)
                        if sol:
                            base_e, tof, delev = sol
                            # Howitzer fires High Arc (Elevation decreases to shoot further)
                            # Higher target -> Needs to shoot further horizontally -> Subtract elevation
                            adj_e = int(round(base_e - (dz / 100.0) * delev))
                            results.append(f"C{c}: ↔ {az_mil} mil / ↕ {adj_e} mil ({tof}s)")
                    if not results: results.append("OUT OF RANGE")
                
                targets.append({
                    'label': tname, 
                    'dist': int(round(dist)),
                    'coord_str': f"X:{tx:.1f} Y:{ty:.1f} Z:{tz:.1f}", 
                    'output': " | ".join(results)
                })
            except: continue

if __name__ == "__main__":
    main()