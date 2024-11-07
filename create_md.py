import os

dirs = [d for d in os.listdir() if os.path.isdir(d) and not d.startswith('.')]

base_github_url = "https://thailand-oi-task-team.github.io/thailand-oi-tasks"

months = {
  "jan": "มกรา", "feb": "กุมภา", "mar": "มีนา",
  "apr": "เมษา", "may": "พฤษภา", "jun": "มิถุนา",
  "jul": "กรกฎา", "aug":"สิงหา", "sep": "กันยา",
  "oct": "ตุลา", "nov": "พฤศจิกา", "dec": "ธันวา"
}

months_to_int = {
  "oct": 1, "nov": 2, "dec": 3,
  "jan": 4, "feb": 5, "mar": 6,
  "apr": 7, "may": 8, "jun": 9,
  "jul": 10, "aug": 11, "sep": 12
}

for d in dirs:
  if d in ["55-56", "56-57", "57-58", "58-59"]:
    continue
  problems = set(f.split('.')[0] for f in os.listdir(d) if f.endswith('.pdf'))
  public_zips = set(f.split('.')[0] for f in os.listdir(d) if f.endswith('.zip'))
  camps = set()
  camp_problem = dict()
  for p in problems:
    camp = None
    day = None
    print(p)
    if len(p.split('_')[1]) == 3:
      if len(p.split('_')) == 3:
        continue
      camp = p.split('_')[1][:3]
      day = int(p.split('_')[2][1])
    elif len(p.split('_')[1]) > 3:
      camp = p.split('_')[1][:3]
      day = int(p.split('_')[1][3:])
    else:
      raise ValueError(f"Invalid problem name: {p}")
    if camp == None or day == None:
      raise ValueError(f"Invalid problem name: {p}")
    camps.add(camp)
    if camp not in camp_problem:
      camp_problem[camp] = dict()
    if day not in camp_problem[camp]:
      camp_problem[camp][day] = list()
    camp_problem[camp][day].append((p, p + "_public" in public_zips))
  camp_list = list(camps)
  camp_list_sorted = sorted(camp_list, key=lambda x: months_to_int[x])

  with open(f"{d}/README.md", "w") as f:
    f.write(f"# ปี 25{d.split('-')[0]} - 25{d.split('-')[1]}\n")
    for camp in camp_list_sorted:
      year = d.split('-')[0 if months_to_int[camp] <= 3 else 1]
      f.write(f'\n## ค่าย{months[camp]} {year}\n')
      for day in sorted(camp_problem[camp].keys()):
        f.write(f'\n### วันที่ {day}\n\n')
        for p in sorted(camp_problem[camp][day]):
          f.write(f"- [{p[0].split('_')[-1].split('.')[0]} (pdf)]({base_github_url}/{d}/{p[0]}.pdf)")
          if p[1]:
            f.write(f" และ [{p[0].split('_')[-1].split('.')[0]} (zip)]({base_github_url}/{d}/{p[0]}_public.zip)\n")
          else:
            f.write('\n')