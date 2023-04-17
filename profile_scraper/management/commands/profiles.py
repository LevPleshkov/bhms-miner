from typing import Any, Optional
from tqdm import tqdm
from pandas import read_csv
from numpy import nan

from django.core.management.base import BaseCommand, CommandParser, CommandError

from profile_scraper.models import Profile, BusinessInfo

from ._utils import _validate_path


class Command(BaseCommand):
    help = "Download profiles stored in the database or upload existing profiles to \
        the database from csv-file that was exported previously with this system."

    def add_arguments(self, parser: CommandParser) -> None:
        parser.add_argument('mode', type=str, choices=['download', 'upload'])
        parser.add_argument('-p', '--path', type=str, required=True,
                            help="Specify path to csv-file with profiles that \
                            were scraped by posts")
        parser.add_argument('-b', '--beg', type=int,
                            help="Specify the first row in csv-file \
                            to upload into database, default is 0",)
        parser.add_argument('-e', '--end', type=int,
                            help="Specify the last row in csv-file \
                            to upload into database, default is len(rows)",)

    def handle(self, *args: Any, **options: Any) -> Optional[str]:
        mode = options['mode']
        if mode == 'upload':
            self._load_profiles(
                options['path'], options['beg'], options['end'])
        else:
            raise CommandError(
                self.style.ERROR('Sorry, only upload functionality is implemented.'),)

    def _load_profiles(self, path: str, beg: int, end: int) -> None:
        if _validate_path(self, path):
            df = read_csv(path)

        df = df.replace(nan, None)
        df['ID'] = df['ID'].astype(int).astype(str)

        profiles_created_cnt = profiles_updated_cnt = 0
        errors = []

        beg = beg if beg else 0
        end = end if end else len(df)
        for idx, row in tqdm(df.iloc[beg:end].iterrows(), total=(end-beg),
                             ncols=100, unit='row', colour='blue'):
            try:
                binfo_obj, _ = BusinessInfo.objects.get_or_create(
                    category=row['Business category'],
                    contact_method=row['Business contact method'],
                    address=row['Business address'],
                    email=row['Business e-mail'],
                    phone=row['Business phone number'],)
                _, created = Profile.objects.get_or_create(
                    external_id=row['ID'],
                    defaults={'username': row['Username'],
                              'full_name': row['Full name'],
                              'biography': row['Biography'],
                              'followers': row['Followers'],
                              'followees': row['Followees'],
                              'category': row['Category'],
                              'profile_pic': row['Profile pic'],
                              'is_business': row['Is business'],
                              'business_info': binfo_obj, },)
                if created:
                    profiles_created_cnt += 1
                else:
                    profiles_updated_cnt += 1
            except Exception as e:
                errors.append(f"Row {idx} could not be updated or " +
                              f"added to database! Reason: {e}")

        if len(errors):
            [self.stdout.write(
                self.style.ERROR(e)) for e in errors]
        self.stdout.write(self.style.SUCCESS(
            f"Inserted {profiles_created_cnt}" +
            f", updated {profiles_updated_cnt}" +
            (f", failed {len(errors)}" if len(errors) else "") +
            " profiles."),)
