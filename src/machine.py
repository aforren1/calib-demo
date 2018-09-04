from transitions import Machine


class IndividuationStateMachine(Machine):
    def __init__(self):
        states = ['pre_trial',  # wait for the space press to start, and show text instruction on the screen
                  # after space press, start countdown timer and show target (5 sec to be within n dist of target)
                  'moving',
                  'hold_in_target',  # restart countdown timer for 1s
                  'post_trial',
                  'post_exp']  # if more than half of time was in target, happy. Remove target and wait ~1s

        pre_trial_t = {'source': 'pre_trial',
                       'trigger': 'step',
                       'conditions': 'wait_for_space',
                       'after': ['start_trial_countdown',
                                 'show_target',
                                 'trial_text'],
                       'dest': 'moving'}
        # prepare
        moving_t = {'source': 'moving',
                    'trigger': 'step',
                    'conditions': 'close_to_target',
                    'after': ['start_hold_countdown',  # wait for 1s
                              'hold_text'],  # Instruct to stay in target
                    'dest': 'hold_in_target'}

        moving_t2 = {'source': 'moving',
                     'trigger': 'step',
                     'conditions': 'time_elapsed',  # check if countdown timer is negative
                     'after': ['hide_target',
                               'start_post_countdown',
                               'increment_trial_counter',
                               'write_trial_data',
                               'post_text'],
                     'dest': 'post_trial'}

        # hold in target
        hold_in_target_t = {'source': 'hold_in_target',
                            'prepare': 'queue_distance',
                            'trigger': 'step',
                            'conditions': 'time_elapsed',
                            'after': ['hide_target',
                                      'start_post_countdown',
                                      'check_distance',  # if managed to hold force, happy sound
                                      'increment_trial_counter',
                                      'write_trial_data',
                                      'post_text'],
                            'dest': 'post_trial'}

        post_trial_t = {'source': 'post_trial',
                        'trigger': 'step',
                        'conditions': ['time_elapsed', 
                                       'trial_counter_exceeded'],
                        'after': 'clean_up',  # run sys.exit
                        'dest': 'post_exp'}

        post_trial_t2 = {'source': 'post_trial',
                         'trigger': 'step',
                         'conditions': 'time_elapsed',
                         'after': ['reset_keyboard_bool', 'kb_text'],
                         'dest': 'pre_trial'}

        transitions = [pre_trial_t, moving_t, moving_t2,
                       hold_in_target_t, post_trial_t, post_trial_t2]
        Machine.__init__(self, states=states,
                         transitions=transitions, initial='pre_trial')
