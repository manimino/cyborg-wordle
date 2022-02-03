import cmd
commands = []
class CmdParse(cmd.Cmd):
    prompt = "> "
    def do_listall(self, line):
        print(commands)
    def default(self, line):
        print(line[::-1])
        commands.append(line)
CmdParse().cmdloop()
