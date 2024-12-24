import json
import os

def existing_jobs():
    '''
    This function reads from your current viewed jobs (that you manually update) from 'existing_jobs.json'
    and returns a python usable list of dictionaries.
    '''
    with open('./output/existing_jobs.json', 'r', encoding='utf-8') as file:
        data = json.load(file)
        data_list = []
        for row in data:
            data_list.append(row)
        return data_list

existing_data = existing_jobs()


def scraped_jobs():
    '''
    This function reads from the scraped jobs from 'scraped_jobs.json' and returns a python usable list of dictionaries.
    '''
    with open('./output/scraped_jobs.json', 'r', encoding='utf-8') as file:
        data = json.load(file)
        data_list = []
        for row in data:
            data_list.append(row)
        return data_list

scraped_data = scraped_jobs()

def job_filter():
    '''
    This function filters the collected jobs and removes any job listings that have key words that you choose to reject.
    '''
    
    # current_skills = ['Python', 'python']
    # missing implementation to filter jobs based on preferred key skills that show up in the job listing

    denied_skills = ['Azure', 'azure', 'C+', 'Databricks', 'NoSql', 'Redshift', 'Snowflake', 'GCP', 'Google Cloud Platform', 'Go', 'R']
    valid_job = True
    filtered_jobs = []
    for jobs in scraped_data:
        for denied_word in denied_skills:
            if denied_word in jobs['description']:
                valid_job = False

        if valid_job == True:   
            filtered_jobs.append(jobs)
        valid_job = True
    return filtered_jobs

new_data = job_filter()
print('new_data : ', new_data)

def duplicate_job_checker(old_jobs, new_jobs):
    '''
    This function checks the new scraped jobs against the existing jobs to prevent any duplicate job listings
    '''
    job_exists = False
    new_jobs_to_add = []
    for new_job in new_jobs:
        for old_job in old_jobs:
            if new_job['description'] == old_job['description']:
                job_exists = True
        if job_exists == False:
            print(f"new job found : {new_job['title']} - {new_job['company']}")
            new_jobs_to_add.append(new_job)
        job_exists = False
    return new_jobs_to_add


def new_job_writer():
    '''
    This function writes the scraped jobs that have been filtered from the above two functions, creating new_jobs.json
    '''
    with open('./output/new_jobs.json', 'w') as file:
        file.write(json.dumps(duplicate_job_checker(existing_data, new_data)))


if os.path.exists("./output/new_jobs.json"):
    os.remove("./output/new_jobs.json")

new_job_writer()


    