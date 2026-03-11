"""Typing tests for zyncio.

This file is expected to pass type checking (with Pyright) without any errors.
The tests are designed to ensure that valid usages have correct types inferred,
and that invalid usages produce type errors.

Expected errors are marked with `# pyright: ignore[...]` comments; `reportUnnecessaryTypeIgnore` will
report lines that unexepectedly pass type checking.
"""

import asyncio
from typing_extensions import assert_type

import zyncio

from .client import AsyncClient, BaseClient, SyncClient


base_client = BaseClient()
sync_client = SyncClient()
async_client = AsyncClient()

base_client.simple_zmethod(1)  # pyright: ignore[reportCallIssue]
assert_type(sync_client.simple_zmethod(1), int)
assert_type(asyncio.run(async_client.simple_zmethod(1)), int)

base_client.simple_zproperty  # pyright: ignore[reportAttributeAccessIssue]
assert_type(sync_client.simple_zproperty, zyncio.Mode)
assert_type(asyncio.run(async_client.simple_zproperty()), zyncio.Mode)

base_client.settable_zproperty  # pyright: ignore[reportAttributeAccessIssue]
assert_type(sync_client.settable_zproperty, int)
sync_client.settable_zproperty = 1
assert_type(asyncio.run(async_client.settable_zproperty()), int)
asyncio.run(async_client.settable_zproperty.set(1))
# This test needs to come last, since the assignment messes with the inferred
# type of `async_client.settable_zproperty`.
async_client.settable_zproperty = 1  # pyright: ignore[reportAttributeAccessIssue]

base_client.class_method()  # pyright: ignore[reportCallIssue]
assert_type(SyncClient.class_method(), type[SyncClient])
assert_type(asyncio.run(AsyncClient.class_method()), type[AsyncClient])
