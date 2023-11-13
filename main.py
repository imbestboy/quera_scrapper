import time
import bs4
import requests
import random


def counter(dictionary: dict, key: str, how_many: int = 1):
    """counter countion in dictionaries

    Arguments:
        dictionary {dict} -- dict you counting something on it
    """
    key = key.lower().strip()
    if key.replace("_", "").replace("-", "").replace(" ", "").isalnum():
        dictionary[key] = dictionary.get(key, 0) + how_many


def show_detail(step: str):
    if can_show_detail:
        print(step)


detail_showing = input("do you want see detail of scrap ? (y/n) : ")
print("\nthis application may takes some minute ...")
can_show_detail = True if detail_showing.startswith("y") else False

# initializing
remote_jobs = job_count = 0
main_technologies, normal_technologies, salaries = (
    dict(),
    dict(),
    dict(),
)
developer_levels = {"senior": 0, "junior": 0, "intern": 0, "lead": 0}
job_times = {"full_time": 0, "part_time": 0, "project": 0}
page = 1

# scraping page by page
while True:
    # making request and parse
    show_detail(f"getting and parsing page {page} ...")
    try:
        response = requests.get(f"https://quera.ir/magnet/jobs?page={page}").content
    except KeyboardInterrupt:
        exit()
    except:
        re = "re"
        if page == 1:
            print("\nconnection lost !")
            re = ""
        print("\nthis application need internet connection to get jobs fine")
        print(f"\nPLEASE {re}CONNECT TO THE INTERNET AND TRY AGAIN")

        input("press enter to close app")
        exit()
    parsed_response = bs4.BeautifulSoup(response, "html.parser")
    # check end pages or not
    is_end = parsed_response.find(class_="chakra-text css-1csxn5y")
    if is_end and is_end.text == "فرصت شغلی با این مشخصات یافت نشد":
        show_detail(f"page {page - 1} was the last one\n")
        break

    # start page scraping
    show_detail(f"getting jobs in page {page} ...")
    jobs = parsed_response.find(class_="chakra-stack css-1536cui")
    for job in jobs:
        if job_count % 16 == 0:
            job_count += 1
            continue
        job_count += 1
        job_technologies = job.find(class_="chakra-stack css-5lzoxc e35d97a1")
        if job_technologies:
            for tech in job_technologies:
                try:
                    if tech["title"] == "تکنولوژی اصلی":
                        counter(main_technologies, tech.text)
                except KeyError:
                    counter(normal_technologies, tech.text)
            information = job.find(class_="chakra-stack css-1iyteef")
            if "امکان دورکاری" in information.text:
                remote_jobs += 1
            spans_in_information = information.find_all("span")
            developer_level, job_time, *_ = spans_in_information
            if "حقوق" in information.text:
                for span in spans_in_information:
                    if "حقوق" in span.text:
                        salary = span.text
                        salary = salary.replace(",", "").replace("حقوق", "").strip()
                        min_salary, max_salary = salary.split("تا")
                        salaries["min"] = salaries.get("min", []) + [int(min_salary)]
                        salaries["max"] = salaries.get("max", []) + [int(max_salary)]
            counter(developer_levels, developer_level.text)
            if job_time.text == "تمام‌وقت":
                key = "full_time"
            elif job_time.text == "پاره‌وقت":
                key = "part_time"
            else:
                key = "project"
            counter(job_times, key)

    sleep_time = random.randint(4, 8)
    show_detail(f"wait {sleep_time} second to get page {page + 1} ...\n")
    time.sleep(sleep_time)

    # end page scraping
    page += 1


# show results

print(f"all available jobs : {job_count - page - 1}")
print(f"remote jobs count : {remote_jobs}")
print(f"remote jobs percent : {(remote_jobs/job_count)*100:.2f}%\n")

print(f"full time jobs count : {job_times['full_time']}")
print(f"full time jobs percent : {(job_times['full_time']/job_count)*100:.2f}%\n")

print(f"part time jobs count : {job_times['part_time']}")
print(f"part time jobs percent : {(job_times['part_time']/job_count)*100:.2f}%\n")

print(f"project base jobs count : {job_times['project']}")
print(f"project base jobs percent : {(job_times['project']/job_count)*100:.2f}%\n")

all_level_developers = (
    developer_levels["junior"]
    + developer_levels["senior"]
    + developer_levels["intern"]
    + developer_levels["lead"]
)
print(f"junior developer count : {developer_levels['junior']}")
print(
    f"junior developer percent : {(developer_levels['junior']/all_level_developers)*100:.2f}%\n"
)

print(f"senior developer count : {developer_levels['senior']}")
print(
    f"senior developer percent : {(developer_levels['senior']/all_level_developers)*100:.2f}%\n"
)

print(f"intern developer count : {developer_levels['intern']}")
print(
    f"intern developer percent : {(developer_levels['intern']/all_level_developers)*100:.2f}%\n"
)

print(f"lead developer count : {developer_levels['lead']}")
print(
    f"lead developer percent : {(developer_levels['lead']/all_level_developers)*100:.2f}%\n"
)

# sort main technologies
technologies_sorted = sorted(
    main_technologies.items(), reverse=True, key=lambda x: x[1]
)

print(f"3 of most popular main technologies :")
for i in range(3):
    print(f"{i+1}- {technologies_sorted[i][0]} ({technologies_sorted[i][1]})")

# sort normal technologies
normal_technologies_sorted = sorted(
    normal_technologies.items(), reverse=True, key=lambda x: x[1]
)
print(f"\n3 of most popular normal technologies :")
for i in range(3):
    print(
        f"{i+1}- {normal_technologies_sorted[i][0]} ({normal_technologies_sorted[i][1]})"
    )
print(
    f"\nsalary avg : min: {int(sum(salaries['min'])/len(salaries['min'])):,} - max: {int(sum(salaries['max'])/len(salaries['max'])):,} from {len(salaries['min'])} jobs\n"
)

input("press enter to close app")
