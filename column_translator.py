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
        "HI": "HISPANIC",
        "AM": "AMERICAN_INDIAN",
        "AS": "ASIAN",
        "HP": "PACIFIC_ISLANDER",
        "BL": "BLACK",
        "WH": "WHITE",
        "TR": "MULTIRACIAL"
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
    # print('process_by_module', part, module)
    result = part

    module_mapper = {
        CRDCModule.Enrollment.value: {
            "PSENR": "PRESCHOOL",
            "LEPENR": "LEP_ENROLLMENT",
            "LEPPROGENR": "LEP_PROGRAM_ENROLLMENT",
            "IDEAENR": "IDEA",
            "504ENR": "504",
        },
        CRDCModule.AlgebraI.value:  {
            "ALGENR": "ENROLLMENT",
            "ALGPASS": "PASSED",
            "ALGCLASSES": "CLASSES_MS",
            "ALGCERT": "CERTIFIED_CLASSES_MS",
            "MATHCLASSES": "CLASSES_HS",
            "MATHCERT": "CERTIFIED_CLASSES_HS",
            "ALG": "",
            "GS0708": "MS"
        },
        CRDCModule.Geometry.value:  {
            "GEOMENR": "ENROLLMENT",
            "MATHCERT": "CERTIFIED_CLASSES_HS",
            "MATHCLASSES": "CLASSES_HS",
        },
        CRDCModule.SingleSexClasses.value:  {
            "ALGG": "CLASSES_ALGEBRA_GEOMETRY",
            "OTHM": "CLASSES_OTHER_MATH",
            "SCI": "CLASSES_SCIENCE",
            "ENGL": "CLASSES_ENGLISH",
            "OTHA": "CLASSES_OTHER_ACADEMIC",
        },
        CRDCModule.AdvancedPlacement.value: {
            "APMATHENR": "MATH",
            "APSCIENR": "SCIENCE",
            "APOTHENR": "OTHER",
            "APEXAM": "EXAM",
            "APPASS": "PASS",
            "APCOURSES": "DIFFERENT_COURSES",
            "APSEL": "SELF_SELECTION",
        },
        CRDCModule.CorporalPunishment.value: {
            "PSCORPINSTANCES": "PRESCHOOL_INSTANCES",
            "CORPINSTANCES": "INSTANCES",
        },
        CRDCModule.Suspensions.value: {
            "SINGOOS": "SINGLE_OOS",
            "MULTOOS": "MULTIPLE_OOS",
            "PSOOSINSTANCES": "PRESCHOOL_OOS_INSTANCES",
            "OOSINSTANCES": "OOS_INSTANCES",
        },
        CRDCModule.Expulsions.value: {
            "EXPWE": "EXPULSION_W_SERVICES",
            "EXPWOE": "EXPULSION_WO_SERVICES",
            "EXPZT": "EXPULSION_ZERO_TOL",
        },
        CRDCModule.ReferralsAndArrests.value: {
            "REF": "REFERRAL",
            "ARR": "ARREST",
        },
        CRDCModule.Offenses.value: {
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
        },
        CRDCModule.RestraintAndSeclusion.value: {
            "MECH": "MECHANICAL",
            "PHYS": "PHYSICAL",
            "SECL": "SECLUSION",
            "RSINSTANCES": "INSTANCES",
        },
        CRDCModule.HarassmentAndBullying.value: {
            "HBALLEGATIONS": "ALLEGATIONS",
            "HBREPORTED": "REPORTED",
            "HBDISCIPLINED": "DISCIPLINED",
            "RAC": "RACE",
            "DIS": "DISABILITY",
            "ORI": "ORIENTATION",
            "REL": "RELIGION"
        },
        CRDCModule.ChronicAbsenteeism.value: {
            "ABSENT": "",
        },
        CRDCModule.SingleSexAthletics.value: {
            "SSSPORTS": "SPORTS",
            "SSTEAMS": "TEAMS",
            "SSPART": "PARTICIPANTS",
        },
        CRDCModule.SchoolExpenditures.value: {
            "WOFED": "WITHOUT_FEDERAL",
            "WFED": "WITH_FEDERAL",
            "SAL": "SALARY",
            "NPE": "NON_PERSONNEL",
            "TEACH": "TEACHERS",
            "TOTPERS": "TOTAL_PERSONNEL",
            "AID": "INSTRUCTIONAL_AIDES",
            "ADM": "ADMIN",
            "SUP": "SUPPORT_STAFF",
        },
        CRDCModule.SchoolSupport.value: {
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
        },
        CRDCModule.JusticeFacility.value: {
            "JJTYPE": "TYPE",
            "JJSYDAYS": "SCHOOL_YEAR_DAYS",
            "JJHOURS": "PROGRAM_HOURS_PER_WEEK",
            "JJPART": "PARTICIPANTS",
            "LT15": "LESS_THAN_15_DAYS",
            "15T30": "15_TO_30_DAYS",
            "31T90": "31_TO_90_DAYS",
            "91T180": "91_TO_180_DAYS",
            "OV180": "OVER_180_DAYS",
        },
    }

    module_switcher = module_mapper.get(module, {})
    result = module_switcher.get(part, result)

    # REMAP COMMON MATH ABBREVIATIONS
    if(CRDCModule.AlgebraII.value or CRDCModule.Calculus.value or CRDCModule.AdvancedMathematics.value):
        math_switcher = {
            "MATHCERT": "CERTIFIED_CLASSES",
            "MATHCLASSES": "CLASSES",
        }
        result = math_switcher.get(part, result)

    # REMAP COMMON SCIENCE ABBREVIATIONS
    if(CRDCModule.Biology.value or CRDCModule.Physics.value):
        sci_switcher = {
            "SCICCERT": "CERTIFIED_CLASSES",
            "SCICLASSES": "CLASSES",
        }
        result = sci_switcher.get(part, result)

    # REMAP COMMON DISCIPLINE ABBREVIATIONS
    discipline_switcher = {
        "PSDISC": "PRESCHOOL",
        "DISCWODIS": "WO_DISIBILITY",
        "DISCWDIS": "W_DISIBILITY"
    }
    result = discipline_switcher.get(part, result)

    # DELETE UNNEEDED PREFIXES
    module_prefixes = [
        "RET", "RS", "OFFENSE", "TFRALT",
        "EXP", "CORP", "SATACT", "IBENR",
        "APENR", "SSCLASSES", "PHYS", "CHEM",
        "SCIENR", "BIOL", "ADVM", "MATHENR",
        "GEOM", "ALG2", "CALC", "DUALENR", "GTENR", "ENR"]

    if(result in module_prefixes):
        result = ""

    return result


def make_meaningful_name(orig, module):
    # print('make_meaningful_name', module)

    result_split = orig.upper().split("_")

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

    cleaned_result = list(filter(lambda x: len(x) > 0, result_split))
    cleaned_result = list(map(lambda x: x.lower(), cleaned_result))
    meaningful_name = "_".join(cleaned_result)

    if(meaningful_name.startswith('504')):
        meaningful_name = meaningful_name.replace('504', 'prog504')

    return meaningful_name
