# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
"""Various constants used by this plugin"""

from sublime import platform, version

PLATFORM = platform()
SUBLIME_VERSION = int(version())

DIAGNOSTICS_MARKER_BEGIN = b"### GvarEdit diagnostics begin ###"
DIAGNOSTICS_MARKER_END = b"### GvarEdit diagnostics end ###"
