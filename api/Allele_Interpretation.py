from api.models import DrugsAndSNP

def carrier_status(drug, pair):
    pairs = DrugsAndSNP.objects.get(drug = drug).pairs
    at_risk_pairs = pairs.split(",")
    cannot_determine = ["D", "I", "_", "-"]
    if True in map(lambda not_a_nucleic_acid: not_a_nucleic_acid in pair, cannot_determine):
        return "cannot determine"
    elif True in map(lambda at_risk_nucleic_acids: at_risk_nucleic_acids == pair, at_risk_pairs):
        return "at risk"
    else:
        return "common"
