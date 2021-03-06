# -*- coding: utf-8 -*-

############################ Copyrights and license ############################
#                                                                              #
# Copyright 2013 Vincent Jacques <vincent@vincent-jacques.net>                 #
#                                                                              #
# This file is part of PyGithub. http://jacquev6.github.com/PyGithub/          #
#                                                                              #
# PyGithub is free software: you can redistribute it and/or modify it under    #
# the terms of the GNU Lesser General Public License as published by the Free  #
# Software Foundation, either version 3 of the License, or (at your option)    #
# any later version.                                                           #
#                                                                              #
# PyGithub is distributed in the hope that it will be useful, but WITHOUT ANY  #
# WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS    #
# FOR A PARTICULAR PURPOSE. See the GNU Lesser General Public License for more #
# details.                                                                     #
#                                                                              #
# You should have received a copy of the GNU Lesser General Public License     #
# along with PyGithub. If not, see <http://www.gnu.org/licenses/>.             #
#                                                                              #
################################################################################

import github.GithubObject


class Status(github.GithubObject.NonCompletableGithubObject):
    """
    This class represents status as defined in https://status.github.com/api
    """

    @property
    def status(self):
        """
        :type: string
        """
        return self._NoneIfNotSet(self._status)

    @property
    def last_updated(self):
        """
        :type: datetime.datetime
        """
        return self._NoneIfNotSet(self._last_updated)

    def _initAttributes(self):
        self._status = github.GithubObject.NotSet
        self._last_updated = github.GithubObject.NotSet

    def _useAttributes(self, attributes):
        if "status" in attributes:  # pragma no branch
            assert attributes["status"] is None or isinstance(attributes["status"], (str, unicode)), attributes["status"]
            self._status = attributes["status"]
        if "last_updated" in attributes:  # pragma no branch
            assert attributes["last_updated"] is None or isinstance(attributes["last_updated"], (str, unicode)), attributes["last_updated"]
            self._last_updated = self._parseDatetime(attributes["last_updated"])
