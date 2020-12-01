from django.core import management
from django_cron import CronJobBase, Schedule


class BackupJob(CronJobBase):
    RUN_EVERY_MINS = 180  # every 3 hours
    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
    code = "insurance.Backup"

    def do(self):
        management.call_command("dbbackup")
