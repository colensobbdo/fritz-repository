import re
import os
import glob
import plistlib
import logging
from invoke import task, Collection
import semver


_logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


def yes(question: str):
    """Prompt user to input y[es]/n[o] to a yes or no question.
    Args:
        question: Question to answer
    Returns: True if yes, False if no.
    """
    answer = input(question + " (y/n): ").lower().strip()

    while answer not in ['y', 'n', 'yes', 'no']:
        print("Input yes or no")
        answer = input(question + "(y/n):").lower().strip()

    if answer.startswith('y'):
        return True
    else:
        return False


def _git_modified_files():
    """Check for modified files on branch.
    Returns: True if modified, False otherwise
    """
    return os.system('git diff-index --quiet HEAD --') != 0


def _update_changelog(new_version: str):
    """Update CHANGELOG.md with user inputted updates.
    Args:
        new_version: semver new version to update.
    """
    if not yes("Update Changelog file?"):
        _logger.info("Not updating Changelog.")
        return

    changes = []
    changes.append(input("[" + str(len(changes) + 1) + "] "))
    while yes("Add another note to CHANGELOG.md?"):
        changes.append(input("[" + str(len(changes) + 1) + "] "))

    template = [
        '',
        '## [{version}]({github_base}/releases/tag/{version})',
        '',
        *['{}. {}'.format(i + 1, change) for i, change in enumerate(changes)],
        ''
    ]
    template = '\n'.join(template).format(
        version=new_version,
        github_base='https://github.com/fritzlabs/swift-framework'
    )

    with open('CHANGELOG.md') as f:
        lines = f.readlines()

    for i, line in enumerate(lines):
        if line == '---\n':
            lines = [*lines[:i + 1], template, *lines[i + 1:]]
            break

    with open('CHANGELOG.md', 'w') as f:
        f.write(''.join(lines))


@task
def update_version(ctx, new_version):
    """Update version number in Podspec and Frameworks."""
    if _git_modified_files():
        _logger.error('Branch must be clean before updating version spec. '
                      'Clean up modified files and try again.')
        return

    _update_changelog(new_version)

    # os.system('git commit -am "Bump to version {}"'.format(new_version))


@task(default=True)
def list_tasks(ctx):
    """Default: Lists all available tasks"""
    ctx.run("invoke --list")