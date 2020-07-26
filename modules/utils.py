
from configparser import ConfigParser
import modules.common_params as g
import requests
import progressbar as pb
import os
import cv2

g.config = {}

def process_config(args):
# parse config file into a dictionary with defaults

    g.config = {}
    has_secrets = False
    secrets_file = None

    def _correct_type(val,t):
        if t == 'int':
             return int(val)
        elif t == 'eval':
            return eval(val) if val else None
        elif t == 'str_split':
            return str_split(val) if val else None
        elif t  == 'string':
            return val
        elif t == 'float':
            return float(val)
        else:
            g.logger.error ('Unknown conversion type {} for config key:{}'.format(e['type'], e['key']))
            return val

    def _set_config_val(k,v):
    # internal function to parse all keys
        val = config_file[v['section']].get(k,v['default'])

        if val and val[0] == '!': # its a secret token, so replace
            g.logger.debug ('Secret token found in config: {}'.format(val));
            if not has_secrets:
                raise ValueError('Secret token found, but no secret file specified')
            if secrets_file.has_option('secrets', val[1:]):
                vn = secrets_file.get('secrets', val[1:])
                #g.logger.debug ('Replacing {} with {}'.format(val,vn))
                val = vn
            else:
                raise ValueError ('secret token {} not found in secrets file {}'.format(val,secrets_filename))


        g.config[k] = _correct_type(val, v['type'])
        if k.find('password') == -1:
            dval = g.config[k]
        else:
            dval = '***********'
        #g.logger.debug ('Config: setting {} to {}'.format(k,dval))

    # main        
    try:
        config_file = ConfigParser(interpolation=None)
        config_file.read(args['config'])
        

        if config_file.has_option('general','secrets'):
            secrets_filename = config_file.get('general', 'secrets')
            g.logger.debug ('secret filename: {}'.format(secrets_filename))
            has_secrets = True
            secrets_file = ConfigParser(interpolation = None)
            try:
                with open(secrets_filename) as f:
                    secrets_file.read_file(f)
            except:
                raise            
        else:
            g.logger.debug ('No secrets file configured')
        # now read config values
       
        for k,v in g.config_vals.items():
            #g.logger.debug ('processing {} {}'.format(k,v))
            if k == 'secrets':
                continue
           
            
            _set_config_val(k,v)
            #g.logger.debug ("done")
        
    

        # Check if we have a custom overrides for this monitor
        
    except Exception as e:
        g.logger.error('Error parsing config:{}'.format(args['config']))
        g.logger.error('Error was:{}'.format(e))
        exit(0)





def draw_bbox(img, bbox, labels, classes, confidence, color=None, write_conf=True):

   # g.logger.debug ("DRAW BBOX={} LAB={}".format(bbox,labels))
    slate_colors = [ 
            (39, 174, 96),
            (142, 68, 173),
            (0,129,254),
            (254,60,113),
            (243,134,48),
            (91,177,47)
        ]
   
    arr_len = len(bgr_slate_colors)
    for i, label in enumerate(labels):
        #=g.logger.debug ('drawing box for: {}'.format(label))
        color = bgr_slate_colors[i % arr_len]
        if write_conf and confidence:
            label += ' ' + str(format(confidence[i] * 100, '.2f')) + '%'
       
        cv2.rectangle(img, (bbox[i][0], bbox[i][1]), (bbox[i][2], bbox[i][3]), color, 2)

        # write text 
        font_scale = 0.8
        font_type = cv2.FONT_HERSHEY_SIMPLEX
        font_thickness = 1
        #cv2.getTextSize(text, font, font_scale, thickness)
        text_size = cv2.getTextSize(label, font_type, font_scale , font_thickness)[0]
        text_width_padded = text_size[0] + 4
        text_height_padded = text_size[1] + 4

        r_top_left = (bbox[i][0], bbox[i][1] - text_height_padded)
        r_bottom_right = (bbox[i][0] + text_width_padded, bbox[i][1])
  
        cv2.putText(img, label, (bbox[i][0] + 2, bbox[i][1] - 2), font_type, font_scale, [255, 255, 255], font_thickness)

    return img
