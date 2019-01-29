from enum import Enum


class CRDCModule(Enum):
    Identification = "Identification"
    SchoolCharacteristics = "School Characteristics"
    Enrollment = "Enrollment"
    GiftedandTalented = "Gifted and Talented"
    DualEnrollment = "Dual Enrollment"
    CreditRecovery = "Credit Recovery"
    AlgebraI = "Algebra I"
    Geometry = "Geometry"
    AlgebraII = "Algebra II"
    Calculus = "Calculus"
    AdvancedMathematics = "Advanced Mathematics"
    Biology = "Biology"
    Chemistry = "Chemistry"
    Physics = "Physics"
    SingleSexClasses = "Single-sex Classes"
    AdvancedPlacement = "Advanced Placement"
    InternationalBaccalaureate = "International Baccalaureate"
    SATandACTExams = "SAT and ACT Exams"
    CorporalPunishment = "Corporal Punishment"
    Suspensions = "Suspensions"
    Expulsions = "Expulsions"
    Transfers = "Transfers"
    ReferralsAndArrests = "Referrals and Arrests"
    Offenses = "Offenses"
    RestraintAndSeclusion = "Restraint and Seclusion"
    HarassmentAndBullying = "Harassment and Bullying"
    ChronicAbsenteeism = "Chronic Absenteeism"
    Retention = "Retention"
    SingleSexAthletics = "Single-Sex Athletics"
    SchoolExpenditures = "School Expenditures"
    SchoolSupport = "School Support"
    JusticeFacility = "Justice Facility"


def strip_sch_prefix(orig): return orig.replace("SCH_", "")


def process_psenr(str): return str.replace("PSENR", "PRESCHOOL")


def process_prefix(part, module):
    result = part

    if(part == "SCH" and module != CRDCModule.Identification.value):
        result = ""

    if(part == "TOT"):
        result = "total"

    return result


GROUP_IDENTIFIERS = ["HI", "AM", "AS", "HP", "BL", "WH", "TR"]


def process_group(part, module):
    group_switcher = {
        "HI": "Hispanic",
        "AM": "AmericanIndian",
        "AS": "Asian",
        "HP": "PacificIslander",
        "BL": "Black",
        "WH": "White",
        "TR": "MultiRacial"
    }

    return group_switcher.get(part, part)


def process_suffix(part, module):
    result = part

    if(part == 'M'):
        result = 'Male'
    elif(part == 'F'):
        result = 'Female'
    elif(part == 'IND'):
        result = 'Indicator'
    elif(part == 'WODIS'):
        result = 'WITHOUT_DISABILITY'
    elif(part == 'TOT'):
        result = 'TOTAL'
    return result


def process_by_module(part, module):
    # print('process_by_module', part, module, CRDCModule.GiftedandTalented.value, module ==
    #       CRDCModule.GiftedandTalented.value)
    result = part

    if(module == CRDCModule.Enrollment.value):
        enrollment_switcher = {
            "PSENR": "PRESCHOOL",
        }
        result = enrollment_switcher.get(part, result)

    elif(module == CRDCModule.AlgebraI.value):
        en_switcher = {
            "ALGENR": "ENROLLMENT",
            "ALGPASS": "PASSED",
        }
        result = en_switcher.get(part, result)

    elif(module == CRDCModule.AdvancedPlacement.value):
        ap_switcher = {
            "APMATHENR": "MATH",
            "APSCIENR": "SCIENCE",
            "APOTHENR": "OTHER",
            "APEXAM": "EXAM",
            "APPASS": "PASS",
        }
        result = ap_switcher.get(part, result)

    # elif(module == CRDCModule.CorporalPunishment.value):
        # result = discipline_switcher.get(part, result)
    elif(module == CRDCModule.Suspensions.value):
        sp_switcher = {
            "SINGOOS": "SINGLE_OOS",
            "MULTOOS": "MULTIPLE_OOS",
        }
        result = sp_switcher.get(part, result)
        # result = discipline_switcher.get(result, result)

    # elif(module == CRDCModule.Expulsions.value):
        # result = discipline_switcher.get(part, result)
    # elif(module == CRDCModule.Transfers.value):
        # result = discipline_switcher.get(part, result)
    # elif(module == CRDCModule.ReferralsAndArrests.value):
        # result = discipline_switcher.get(part, result)
    elif(module == CRDCModule.Offenses.value):
        o_switcher = {
            "BATT": "SEXUAL_ASSAULT",
            "ROBWW": "ROBBERY_WITH_WEAPON",
            "ROBWX": "ROBBERY_WITH_FIREARM_EXPLOSIVE",
            "ROBWOW": "ROBBERY_WITHOUT_WEAPON",
            "ATTWW": "ATTACK_WITH_WEAPON",
            "ATTWX": "ATTACK_WITH_FIREARM_EXPLOSIVE",
            "ATTWOW": "ATTACH_WITHOUT_WEAPON",
            "THRWW": "THREAT_WITH_WEAPON",
            "THRWX": "THREAT_WITH_FIREARM_EXPLOSIVE",
            "THRWOW": "THREAT_WITHOUT_WEAPON",
            "POSSWX": "POSSESION_FIREARM_EXPLOSIVE"
        }
        result = o_switcher.get(part, result)
    elif(module == CRDCModule.RestraintAndSeclusion.value):
        rs_switcher = {
            "MECH": "MECHANICAL",
            "PHYS": "PHYSICAL",
            "SECL": "SECLUSION",
            "RSINSTANCES": "NUM",

        }
        result = rs_switcher.get(part, result)
    elif(module == CRDCModule.HarassmentAndBullying.value):
        rs_switcher = {
            "HBALLEGATIONS": "ALLEGATIONS",
            "HBREPORTED": "REPORTED",
            "HBDISCIPLINED": "DISCIPLINED",
            "RAC": "RACE",
            "DIS": "DISABILITY",
            "ORI": "ORIENTATION",
            "REL": "RELIGION"
        }
        result = rs_switcher.get(part, result)
    elif(module == CRDCModule.ChronicAbsenteeism.value):
        ca_switcher = {
            "ABSENT": "",
        }
        result = ca_switcher.get(part, result)
    elif(module == CRDCModule.SingleSexAthletics.value):
        ssa_switcher = {
            "SSSPORTS": "SPORTS",
            "SSTEAMS": "TEAMS",
            "SSPART": "PARTICIPANTS",
        }
        result = ssa_switcher.get(part, result)
    elif(module == CRDCModule.SchoolExpenditures.value):
        se_switcher = {
            "WOFED": "WITHOUT_FEDERAL",
            "WFED": "WITH_FEDERAL",
            "SAL": "SALARY",
            "NPE": "NON_PERSONNEL",
            "TEACH": "TEACHERS",
            "TOTPERS": "TOTAL_PERSONNEL",
            "AID": "INSTRUCTIONAL_AIDES",
            "ADM": "ADMIN",
            "SUP": "SUPPORT_STAFF",
        }
        result = se_switcher.get(part, result)
    elif(module == CRDCModule.SchoolSupport.value):
        ss_switcher = {
            "FTETEACH": "TEACHERS",
            "FTECOUNSELORS": "COUNSELORS",
            "FTESECURITY": "SECURITY",
            "FTESERVICES": "SERVICES",
            "CERT": "CERTIFIED",
            "NONCERT": "NONCERTIFIED",
            "FY": "FIRST_YEAR",
            "SY": "SECOND_YEAR",
            "LEO": "LAW_ENFORCEMENT_OFFICES",
            "GUA": "SECURITY_GUARDS",
            "NUR": "NURSES",
            "PSY": "PSYCHOLOGISTS",
            "SOC": "SOCIAL_WORKERS",
        }
        result = ss_switcher.get(part, result)
    elif(module == CRDCModule.JusticeFacility.value):
        jf_switcher = {
            "JJTYPE": "TYPE",
            "JJSYDAYS": "SCHOOL_YEAR_DAYS",
            "JJHOURS": "PROGRAM_HOURS_PER_WEEK",
            "JJPART": "PARTICIPANTS",
            "LT15": "LESS_THAN_15_DAYS",
            "15T30": "15_TO_30_DAYS",
            "31T90": "31_TO_90_DAYS",
            "91T180": "91_TO_180_DAYS",
            "OV180": "OVER_180_DAYS",
        }
        result = jf_switcher.get(part, result)

    # REMAP COMMON DISABILITY ABBREVIATES
    discipline_switcher = {
        "PSDISC": "PRESCHOOL",
        "DISCWODIS": "WITHOUT_DISIBILITY",
        "DISCWDIS": "WITH_DISIBILITY"
    }
    result = discipline_switcher.get(part, result)

    # DELETE UNNEEDED PREFIXES
    module_prefixes = ["RET", "RS", "OFFENSE", "TFRALT", "EXP", "CORP", "SATACT", "IBENR", "APENR", "SSCLASSES", "PHYS", "CHEM", "SCIENR", "BIOL", "ADVM", "MATHENR", "GEOM", "ALG2",
                       "CALC", "DUALENR", "GTENR", "ENR"]

    if(result in module_prefixes):
        result = ""

    return result


def downcase(word):
    return word[:1].lower() + word[1:] if word else ''


def make_meaningful_name(orig, module):
            # print('make_meaningful_name', module,
            #       module == CRDCModule.Identification.value)
    result_split = orig.split("_")

    for index, part in enumerate(result_split):
            # print(f"\nProcessing {part} at index {index}")
        processed_part = part
        # --- Prefix
        if(index == 0):
            processed_part = process_prefix(processed_part, module)

        # --- Second to Last
        elif(len(result_split) - 2 == index and processed_part in GROUP_IDENTIFIERS):
            processed_part = process_group(processed_part, module)

        # --- Suffix
        elif(len(result_split) - 1 == index):
            processed_part = process_suffix(processed_part, module)

        result_split[index] = process_by_module(processed_part, module)

    # print(result_split)
    cleaned_result = list(filter(lambda x: len(x) > 0, result_split))
    cleaned_result = list(map(lambda x: x.upper(), cleaned_result))
    # print(cleanedResult)
    # camel_cased = ""
    # for index, part in enumerate(cleaned_result):
    #     if(index == 0 and not part.isupper()):
    #         camel_cased = downcase(part)
    #     else:
    #         camel_cased = part.capitalize()
    # print(camel_cased)

    # "_".join(result_sp lit)
    return "_".join(cleaned_result)


def module_to_table_name(module): return module.replace(
    ' ', '_').replace('-', '_').lower()
