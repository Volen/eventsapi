from deta import Deta

def get_all_events_words(deta: Deta):
  event_dict_table = deta.Base('event_dict')
  return event_dict_table.fetch().items