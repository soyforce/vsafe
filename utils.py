import pandas as pd


def expand_multichoice(df: pd.DataFrame, col: str, sep: str = ':', drop: bool = True):
    '''
    Extract choices of a multiple choice column and make bool columns for each choice.
    
    Example:
        >> df.columns
        Index(['PetsOwned'], dtype=object)
        >> df['PetsOwned'].unique()
        array(['Dog', 'Cat', 'Dog:Cat', 'Cat:Bird', 'Bird', 'Dog:Cat:Bird', 'Dog:Bird'], dtype=object)
        >> df = expand_multichoice(df, 'PetsOwned')
        >> df.columns
        Index(['Dog', 'Cat', 'Bird'], dtype=object)
    
    '''
    df = df.copy()
    # Get all unique choice selections, ignores NaN
    vals = [a for a in df[col].unique() if isinstance(a, str)]
    # Separated out gives us each individual multichoice option
    uniques = {k for e in vals for k in e.split(sep)}

    # Make a new column for each choice
    for choice in sorted(uniques):
        # This choice is only True if it was actually in the string
        # Without the isnull check, NaN rows would resolve to True
        mask = ~df[col].isnull() & df[col].str.contains(choice)
        df[choice] = mask.astype(bool)

    if drop:
        df = df.drop(col, axis=1)
    return df
