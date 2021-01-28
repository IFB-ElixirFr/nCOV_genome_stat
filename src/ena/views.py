from statistics import mean

import numpy as np
from django.shortcuts import render, redirect
import apiENA


def redirect_index(request):
    return redirect("dashboardENA",days_range=30)


def dashboard(request, days_range=60, country_names=None):
    days, submits, subByCountries, map = apiENA.get_nb_submits_days(days=days_range, country_names=country_names)

    page_label_time = {7: "Week", 30: "Month", 365: "Year"}.get(days_range, "Custom")

    if country_names:
        page_label_loc = country_names
    else:
        page_label_loc = "World"

    return render(request, "ena/index.html", context={"data": submits,
                                                      "dataCum": np.cumsum(submits).tolist(),
                                                      "daysLabels": days,
                                                      "page_label_loc": page_label_loc,
                                                      "page_label_time": page_label_time,
                                                      "difCountries": len(subByCountries),
                                                      "all_summits": sum(submits),
                                                      "map": map,
                                                      "mean_summits": round(mean(submits))})
