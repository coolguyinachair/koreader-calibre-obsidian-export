import re
import os
import json
import pprint
import sqlite3 as sqlite
from collections import defaultdict

# global values
db_path = r'D:\zcalibre\metadata.db'
export_path = r'D:\knowledge base\notes\sources\books'


# convert book title to safe filename
def sanitize(filename):
    sanitized = filename

    # Remove unsafe characters
    sanitized = re.sub(r'[<>:"/\\|?*\x00-\x1F]', '', sanitized)

    # Handle reserved filenames in Windows
    reserved_names = r'^(con|prn|aux|nul|com[0-9]|lpt[0-9])(\..*)?$'
    sanitized = re.sub(reserved_names, r'_\1\2', sanitized, flags=re.IGNORECASE)

    # Remove trailing whitespace and dots
    sanitized = re.sub(r'[\s.]+$', '', sanitized)

    # Replace leading dots
    sanitized = re.sub(r'^\.', '_', sanitized)

    return sanitized


def main():

    # sqlite connection
    con = sqlite.connect(f"file:{db_path}?mode=ro", uri=True)
    cur = con.cursor()

    # fetch list of finished books
    cur.execute('select * from custom_column_9 where value=1;')
    rows = cur.fetchall()
    book_ids = [row[1] for row in rows]

    # for each finished book
    for book_id in book_ids:

        # fetch book title
        cur.execute(f'select title from books where id={book_id}')
        bookname = cur.fetchone()[0]
        print(f'Processing {bookname}.')

        # get safe filename from book title
        bookname = sanitize(bookname)
        filename = bookname.lower()

        # if annotations for book already exported (file already exists)
        if os.path.exists(os.path.join(export_path, f'{filename}.md')):
            print(f'{filename}.md already exists in vault')
            continue

        # fetch authors
        cur.execute(f'select author_sort from books where id={book_id}')
        authors = '\n'.join(['  - ' + ' '.join(reversed(auth.split(', '))) for auth in cur.fetchall()[0][0].split(' & ')])

        # fetch sidecar contents
        cur.execute(f'select value from custom_column_8 where book={book_id}')
        res = cur.fetchone()[0]
        annotations = json.loads(res)['annotations']

        annotations_by_chapters = defaultdict(list)

        # for each annotation
        print('fetching annotations')
        for idx in annotations:

            anno = annotations[idx]

            # if bookmark, skip
            if not anno.get('pos0', False):
                continue

            # fetch annotation details
            chapter = anno.get('chapter', 'Unknown highlight')

            highlighted_text = ['> ' + re.sub("[<>]", '', s.rstrip(r'\\')) for s in anno.get('text', 'Unknown highlight.').split('\n')]
            highlighted_text = '\n'.join(['>[!quote]'] + highlighted_text)

            notes = anno.get('note', '')
            if notes:
                notes = ['- ' + s.rstrip(r'\\') for s in notes.split('\n')]
                notes = '\n' + '\n'.join(notes)

            # categorize annotations by chapters
            annotations_by_chapters[chapter].append([highlighted_text, notes])

        # write to markdown file for book in obsidian vault
        print('writing to markdown file')
        with open(os.path.join(export_path, f'{filename}.md'), 'a', encoding='utf-8') as md_file:

            # yaml header
            md_file.write(f'---\nauthor:\n{authors}\naliases:\n  - "{bookname}"\ntags:\n- unparsed\n---\n')

            # format contents
            md_file.write(f'# {bookname}\n\n')
            for chapter, chapter_annotations in annotations_by_chapters.items():
                md_file.write(f'## {chapter}\n\n')
                for highlighted_text, notes in chapter_annotations:
                    md_file.write(f'{highlighted_text}{notes}\n\n')

    con.close()


if __name__ == '__main__':
    main()