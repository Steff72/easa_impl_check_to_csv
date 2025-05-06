import csv


def export_to_csv(results, output_path):
    """
    Save the mapping results to a CSV file with columns:
    Regulation;Dokumentreferenz
    """
    with open(output_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f, delimiter=';')
        writer.writerow(['Regulation', 'Dokumentreferenz'])
        for r in results:
            writer.writerow([r['regulation'], r['section']])