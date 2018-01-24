import json, csv


def load_patterns(filename):
    with open(filename) as f:
        return json.loads(f.read())


def export_to_csv(data, headers, filename):
    with open(filename, 'w') as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=headers)

        writer.writeheader()
        for row in data:
            writer.writerow(row)


def export_to_r(data, filename):
    with open(filename, 'w') as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=["batch", "smell", "percentage"])

        writer.writeheader()
        for row in data:
            r_row = {"batch": ",".join(row["batch"])}
            if r_row["batch"] == "Rename Method":
                continue
            for smell in row:
                if smell == "batch":
                    continue
                r_row["smell"] = smell
                r_row["percentage"] = row[smell]*100
                writer.writerow(r_row)


def summary(filename, pattern_type):  # pattern_type = introduced or removed
    data = load_patterns(filename)
    stats = []
    smells_names = set()
    for pattern in data:
        row = {"batch": [",".join(pattern["sequence"])]}
        occurrences = pattern["occurrences"]
        for smell, interference in pattern["interferences"].iteritems():
            smells_names.add(smell)
            # print interference
            percentage = float(interference[pattern_type])/occurrences
            if percentage >= 0.1:
                row[smell] = percentage
        stats.append(row)

    headers = ["batch"] + sorted(list(smells_names))
    filename = "summaries/" + filename.split("/")[-1][:-5] + "_" + pattern_type + ".csv"
    export_to_csv(stats, headers, filename)
    #export_to_r(stats, filename)


summary("interferences/element_based.json", "introduced")
summary("interferences/element_based.json", "removed")
summary("interferences/scope_based.json", "introduced")
summary("interferences/scope_based.json", "removed")
summary("interferences/version_based.json", "introduced")
summary("interferences/version_based.json", "removed")
