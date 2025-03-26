def check_data_array(values_old, values_new):
    # if len(values_old) != len(values_new):
    #     return ["ERROR"]
    changed_values = []
    for i in range(len(values_new)):
        if values_new[i]["Status"]:

            if (
                values_old[i]["Value"] != values_new[i]["Value"]
                or values_old[i]["Signal"] != values_new[i]["Signal"]
            ):  # or values_old[i]["Status"] != values_new[i]["Status"]) :
                changed_values.append(
                    {
                        "Number": i,
                        "Value": values_new[i]["Value"],
                        "Signal": values_new[i]["Signal"],
                        "Status": values_new[i]["Status"],
                    }
                )
    # if len(changed_values) < 100:
    #     for i in changed_values:
    #         print(
    #             f"old {values_old[i["Number"]]["Value"]}{values_old[i["Number"]]["Signal"]} new {i["Value"]}{i["Signal"]}, index: {i["Number"]}",
    #             file=open("logs/parampyrym.txt", "a+"),
    #         )
    # print("", end="\n\n\n", file=open("logs/parampyrym.txt", "a+"))
    return changed_values
