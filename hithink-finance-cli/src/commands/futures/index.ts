import type { Command } from 'commander';
import type { CliContext } from '../../cli/context.js';
import { remoteCapabilities } from '../../contracts/remote-capabilities.js';
import { registerRemoteCapabilityGroup, type RemoteCommandDependencies } from '../remote.js';

export function registerFuturesCommands(
  program: Command,
  context: CliContext,
  dependencies: RemoteCommandDependencies,
): void {
  registerRemoteCapabilityGroup(
    program,
    'futures',
    remoteCapabilities.filter((item) => item.command[0] === 'futures'),
    context,
    dependencies,
  );
}
