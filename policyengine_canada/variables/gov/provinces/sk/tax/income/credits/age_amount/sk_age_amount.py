from policyengine_canada.model_api import *


class sk_age_amount(Variable):
    value_type = float
    entity = Person
    label = "Saskatchewan age amount credit"
    unit = CAD
    definition_period = YEAR
    reference = (
        "https://www.canada.ca/content/dam/cra-arc/formspubs/pbg/td1sk/td1sk-22e.pdf",
        "https://www.canada.ca/content/dam/cra-arc/formspubs/pbg/td1sk/td1sk-23e.pdf",
        "https://www.canada.ca/content/dam/cra-arc/formspubs/pbg/td1-ws/td1-ws-22e.pdf",
        "https://www.canada.ca/content/dam/cra-arc/formspubs/pbg/td1-ws/td1-ws-23e.pdf",
        "https://publications.saskatchewan.ca/api/v1/products/583/formats/806/download",
    )
    defined_for = ProvinceCode.SK

    def formula(person, period, parameters):
        p = parameters(period).gov.provinces.sk.tax.income.credits.age_amount
        income = person("individual_net_income", period)
        age = person("age", period)
        age_eligible = age >= p.age_eligibility
        reduction = p.reduction.rate.calc(income)
        reduced_amount = max_(p.max_amount - reduction, 0)
        is_head = person("is_head", period)
        eligible = is_head & age_eligible
        return eligible * reduced_amount
