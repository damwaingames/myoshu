# `myoshu`

Myoshu (妙手) a CLI for playing Go.

**Usage**:

```console
$ myoshu [OPTIONS] COMMAND [ARGS]...
```

**Options**:

* `--install-completion`: Install completion for the current shell.
* `--show-completion`: Show completion for the current shell, to copy it or customize the installation.
* `--help`: Show this message and exit.

**Commands**:

* `delete`: Delete the game with a given id.
* `list`: List all games.
* `new`: Create a new game.
* `proverb`: Display a random Go proverb.

## `myoshu delete`

Delete the game with a given id. !WARNING! - This cannot be undone.

**Usage**:

```console
$ myoshu delete [OPTIONS] ID
```

**Arguments**:

* `ID`: [required]

**Options**:

* `--help`: Show this message and exit.

## `myoshu list`

List all games.

**Usage**:

```console
$ myoshu list [OPTIONS]
```

**Options**:

* `--all`: Include games that have been completed.
* `--help`: Show this message and exit.

## `myoshu new`

Create a new game.

**Usage**:

```console
$ myoshu new [OPTIONS]
```

**Options**:

* `--boardsize INTEGER`: Size of board to create game on.  [default: 19]
* `--p1-name TEXT`: Name of black player.  [default: Black player]
* `--p2-name TEXT`: Name of white player.  [default: White player]
* `--handicap INTEGER`: Number of handicap stones to be placed.  [default: 0]
* `--help`: Show this message and exit.

## `myoshu proverb`

Display a random Go proverb.

**Usage**:

```console
$ myoshu proverb [OPTIONS]
```

**Options**:

* `--help`: Show this message and exit.
