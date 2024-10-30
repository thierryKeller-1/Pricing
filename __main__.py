import argparse
from datetime import datetime, timedelta
from apps.booking import booking_initializer, booking_starter


def main_arguments() -> object:

    def get_monday():
        return str((datetime.now() - timedelta(days = datetime.now().weekday())).strftime("%d/%m/%Y"))

    def validate_params(args:object) -> None:
        pass

    parser = argparse.ArgumentParser(description="Pricing program",formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('--platform', '-p', dest='platform', help="Site source")
    parser.add_argument('--action', '-a', dest='action', help="""TAction to do: \n \t 'init': initialize destination's urls. | 'start': Launch scraps. | 'clean': clean scrapped datas""")
    parser.add_argument('--weekscrap', '-w', dest='weekscrap', default=get_monday(), help="Monday date of the week to scrap 'dd/mm/YYYY'")
    parser.add_argument('--name', '-n', dest='name', help="name to be used for this instance like output file name")
    
    return parser.parse_args()


args = main_arguments()
print(args)

match args.platform:
    case 'booking':
        if args.action == 'init':
            booking_initializer(args.weekscrap)
        if args.action == 'start':
            #add driver number to the params
            booking_starter(args.weekscrap, args.name)
        if args.action == 'clean':
            pass
    case 'maeva':
        pass
    case 'campings':
        pass
    case 'edomizil':
        pass