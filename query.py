from psrqpy import QueryATNF
import logging

def query_atnf(output_file: str = 'atnf.txt') -> int:
    """
    Query the ATNF pulsar database and save specific pulsar parameters to a file.

    Parameters:
    - output_file: The file where the results will be saved (default is 'atnf.txt').

    Returns:
    - The number of pulsar entries saved to the file.
    """
    try:
        # Set up logging to track progress
        logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
        logging.info('Querying ATNF database...')
        
        # Query the ATNF database
        # url: https://www.atnf.csiro.au/research/pulsar/psrcat/psrcat_help.html
        # P0:          Barycentric period of the pulsar (s)
        # P1:          Time derivative of barycentric period (dimensionless)
        # DM:          Dispersion measure (cm-3 pc)
        # DIST:        Best estimate of the pulsar distance using the YMW16 DM-based distance as default (kpc)
        # ZZ:          Distance from the Galactic plane, based on Dist
        # XX:          X-Distance in X-Y-Z Galactic coordinate system (kpc)
        # YY:          Y-Distance in X-Y-Z Galactic coordinate system (kpc)
        # [DERIVED PARAMETERS]
        # AGE:         Spin down age (yr) [tau = P0 / (2 * P1)]
        # BSurf:       Surface magnetic flux density (Gauss) [B = 3.2 x 10^19 (P_0 P_1)^1/2]
        # Edot:        Spin down energy loss rate (ergs/s)

        query = QueryATNF(params=['P0', 'P1', 'DM', 'DIST', 'ZZ', 'XX', 'YY', 'TYPE'])
        t = query.table
        logging.info('Query successful!')

        # Write query results to the output file
        counter = 0
        with open(output_file, 'w') as file:
            file.write(f'# P0 - P1 - DIST - XX - YY - ZZ\n')
            for row in t:
                P0 = row['P0']
                P1 = row['P1']
                DIST = row['DIST']
                XX = row['XX']
                YY = row['YY']
                ZZ = row['ZZ']
                TYPE = row['TYPE']

                # Check for valid data entries and format the output
                if P0 != '--' and P1 != '--' and DIST != '--':
                    file.write(f'{P0:10.5e} {P1:10.5e} {DIST:10.3f} {XX:10.3f} {YY:10.3f} {ZZ:10.3f} {TYPE}\n')
                    counter += 1

        logging.info(f'Successfully saved {counter} objects to {output_file}.')
        return counter

    except Exception as e:
        logging.error(f"An error occurred: {e}")
        return 0


def main():
    """
    Main function to query the ATNF pulsar database and save results to a file.
    """
    output_file = 'atnf.txt'
    total_saved = query_atnf(output_file)
    print(f"Saved {total_saved} objects to {output_file}.")

if __name__ == '__main__':
    main()
