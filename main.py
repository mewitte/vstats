from argparse import ArgumentParser

from vstats_scout_match.scout_match import scout

def main(match_directory):
  scout(match_directory)

if __name__ == "__main__":
  parser = ArgumentParser(
    prog='VolleyballStats',
    description='Create statistics sheet for a volleyball match'
  )
  parser.add_argument('match_directory')
  args = parser.parse_args()
  main(args.match_directory)
