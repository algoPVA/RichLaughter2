import os
import pandas as pd
import numpy as np


def convert_timeframe(df, timeframe, agg_rules=None, datetime_col='ms', recalc_direction=True, recalc_middle=True) -> pd.DataFrame:
    """
    Универсальная функция для агрегации временных рядов в заданный таймфрейм.
    
    Параметры:
    ----------
    df : pandas.DataFrame
        Входной DataFrame с временным рядом
    timeframe : str
        Строка интервала агрегации (например, '5min', '1H', '1D')
    agg_rules : dict, optional
        Словарь с правилами агрегации для каждого столбца.
        По умолчанию: стандартные правила для OHLCV данных
    datetime_col : str, optional
        Название столбца с датой/временем (по умолчанию 'ms')
    recalc_direction : bool, optional
        Пересчитывать ли направление свечи (по умолчанию True)
    recalc_middle : bool, optional
        Пересчитывать ли середину свечи (по умолчанию True)
    
    Возвращает:
    -----------
    pandas.DataFrame
        DataFrame с агрегированными данными
    """
    
    # Стандартные правила агрегации, если не заданы пользователем
    default_agg_rules = {
        'open': 'first',
        'close': 'last',
        'high': 'max',
        'low': 'min',
        'vol_coin': 'sum',
        'volume': 'sum',
        'direction': 'last',
        'middle': 'last',
        'x': 'last'
    }
    
    # Объединяем пользовательские правила с стандартными (пользовательские имеют приоритет)
    if agg_rules is None:
        agg_rules = default_agg_rules
    else:
        for col in default_agg_rules:
            if col not in agg_rules:
                agg_rules[col] = default_agg_rules[col]
    
    # Копируем DataFrame, чтобы не изменять исходный
    df = df.copy()
    
    # --- НОВЫЙ КОД: АВТОДЕТЕКТ И ПРЕОБРАЗОВАНИЕ ФОРМАТА ДАТЫ ---
    def convert_to_datetime(series):
        """
        Умное преобразование временного ряда в datetime.
        Определяет формат автоматически: timestamp (мс/с) или строки.
        """
        # Проверяем, является ли серия уже datetime
        if pd.api.types.is_datetime64_any_dtype(series):
            return series
            
        # Пробуем определить, являются ли данные числовыми (timestamp)
        if pd.api.types.is_numeric_dtype(series):
            # Определяем масштаб: если числа очень большие (>1e12) - это мс, иначе - секунды
            sample_value = series.iloc[0] if len(series) > 0 else 0
            if sample_value > 1e12:  # Это миллисекунды
                return pd.to_datetime(series, unit='ms')
            else:  # Это секунды
                return pd.to_datetime(series, unit='s')
        else:
            # Пробуем преобразовать строки стандартным методом
            try:
                return pd.to_datetime(series)
            except:
                # Если не получается, пробуем парсить как timestamp в строковом формате
                try:
                    return pd.to_datetime(series.astype(np.int64), unit='ms')
                except:
                    raise ValueError(f"Не удалось преобразовать столбец {datetime_col} в datetime")
    
    # Преобразуем столбец времени в корректный datetime формат
    df[datetime_col] = convert_to_datetime(df[datetime_col])
    # --- КОНЕЦ НОВОГО КОДА ---
    
    # Устанавливаем временной столбец в качестве индекса
    df.set_index(datetime_col, inplace=True)
    
    # Агрегируем данные по заданному интервалу
    df_resampled = df.resample(timeframe).agg(agg_rules).dropna()
    
    # Пересчитываем дополнительные поля, если нужно
    if recalc_direction and 'open' in df_resampled and 'close' in df_resampled:
        df_resampled['direction'] = (df_resampled['close'] - df_resampled['open']).apply(
            lambda x: 1 if x >= 0 else -1)
    
    if recalc_middle and 'high' in df_resampled and 'low' in df_resampled:
        df_resampled['middle'] = (df_resampled['high'] + df_resampled['low']) / 2
    # Сбрасываем индекс, чтобы временной столбец снова стал обычным столбцом
    df_resampled.reset_index(inplace=True)
    df_resampled['ms'] = pd.to_datetime(df_resampled['ms'])
    df_resampled['weekday'] = df_resampled['ms'].dt.dayofweek
    df_resampled['hour'] = df_resampled['ms'].dt.hour
    df_resampled['minute'] = df_resampled['ms'].dt.minute
    
    # Обновляем индексный столбец x, если он есть в данных
    if 'x' in df_resampled:
        df_resampled['x'] = df_resampled.index
    
    return df_resampled

if __name__ == "__main__":
    # folder = 'DataForTests\DataFromMOEX'
    folder = 'data_for_tests\data_from_moex'
    # folder = 'DataForTests\otherMOEX'
    listdir = os.listdir(folder)
    output_folder = 'data_for_tests\data_from_moex5'
    # output_folder = folder
    save_format = '.parquet'
    # save_format = '.csv'
    for f in listdir:
        filepath = os.path.join(folder,f)
        if filepath.endswith('.parquet'):
            df = pd.read_parquet(filepath)
        else:
            df = pd.read_csv(filepath)
        # df = convert_chart1to5(df)
        df = convert_timeframe(df,'5min')
        new_path = os.path.join(output_folder,'_5'+f)
        if save_format == '.csv':
            new_path = new_path.replace('.parquet','.csv')
            df.to_csv(new_path)
        if save_format == '.parquet':
            new_path = new_path.replace('.csv','.parquet')
            df.to_parquet(new_path)
