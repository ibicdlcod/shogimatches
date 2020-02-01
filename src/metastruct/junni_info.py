from metastruct import kishi_data


class JunniInfo:
    iteration: int
    tier: str
    junni: int
    kishi: kishi_data.Kishi
    relegation_point_added: bool
    current_relegation_point: int
    result: str
    to_fc_year: int

    def __init__(self,
                 iteration,
                 tier,
                 junni,
                 kishi,
                 relegation_point_added,
                 current_relegation_point,
                 result,
                 to_fc_year):
        self.iteration = iteration
        self.tier = tier
        self.junni = junni
        self.kishi = kishi
        self.relegation_point_added = relegation_point_added
        self.current_relegation_point = current_relegation_point
        self.result = result
        self.to_fc_year = to_fc_year