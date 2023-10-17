from policyengine_canada.model_api import *


class ns_age_amount_supplement(Variable):
    value_type = float
    entity = Person
    label = "Nova Scotia Age Amount Supplement"
    unit = CAD
    definition_period = YEAR
    defined_for = ProvinceCode.NS
    reference = (
        "https://hr.acadiau.ca/files/sites/hr/Payroll/Pensions%20&%20Benefits/NS_TD1_2022.pdf#page=1",
        "https://www.canada.ca/content/dam/cra-arc/formspubs/pbg/td1ns-ws/td1ns-ws-23e.pdf#page=1",
        "https://nslegislature.ca/sites/default/files/legc/statutes/income%20tax.pdf#page=28",
    )

    def formula(person, period, parameters):
        p = parameters(period).gov.provinces.ns.tax.income.credits.age
        age = person("age", period)
        taxable_income = person("ns_taxable_income", period)

        # is eligible for age amount supplement
        eligibility = age >= p.age_eligibility

        # Calculate additional amount added to base amount
        reduced_additional_amount = max_(
            0,
            p.supplement.base
            - p.supplement.phase_out_rate.calc(taxable_income),
        )

        return eligibility * reduced_additional_amount
