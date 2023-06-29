import uuid
import tempfile
from graphviz import Digraph
from ocpa.objects.oc_petri_net.obj import ObjectCentricPetriNet

COLORS = ['#7f66ff',
          '#ff3399',
          '#f58b55',
          '#f25e65',
          '#261926',
          '#ddb14d',
          '#5387d5',
          '#1c3474',
          '#a37554',
          '#8bc34a',
          '#cddc39',
          '#ffeb3b',
          '#ffc107',
          '#ff9800',
          '#ff5722',
          '#795548',
          '#9e9e9e',
          '#607d8b',
          '#9affff',
          '#000000']


def apply(obj, parameters=None):
    if parameters is None:
        parameters = {}

    image_format = "png"
    if "format" in parameters:
        image_format = parameters["format"]

    filename = tempfile.NamedTemporaryFile(suffix='.gv').name

    g = Digraph("", filename=filename, engine='dot',
                graph_attr={'bgcolor': 'transparent'})
    if "ratio" in parameters:
        ratio = parameters["ratio"]
        g.attr(ratio=ratio)
    all_objs = {}
    trans_names = {}

    pl_count = 1
    tr_count = 1
    arc_count = 1

    # color = COLORS[index % len(COLORS)]
    color = "#05B202"
    color_mapping = dict()
    object_types = obj.object_types
    for index, ot in enumerate(object_types):
        color_mapping[ot] = COLORS[index % len(COLORS)]

    for pl in obj.places:
        this_uuid = str(uuid.uuid4())
        # this_uuid = "p%d" % (pl_count)
        # pl_str = this_uuid
        pl_label = ''.join(w[0].upper() for w in pl.name.split())
        pl_label = pl.name
        pl_count += 1
        color = color_mapping[pl.object_type]
        if pl.initial == True:
            g.node(this_uuid, pl_label, shape="circle", style="filled", fillcolor=color, color=color,
                   fontsize="13.0", labelfontsize="13.0")
        elif pl.final == True:
            g.node(this_uuid, pl_label, shape="circle", style="filled", color=color, fillcolor=color,
                   fontsize="13.0", labelfontsize="13.0")
        else:
            g.node(this_uuid, pl_label, shape="circle", color=color,
                   fontsize="13.0", labelfontsize="13.0")
        all_objs[pl] = this_uuid

    for tr in obj.transitions:
        this_uuid = str(uuid.uuid4())
        tr_count += 1
        if tr.silent == True:
            g.node(this_uuid, "", fontcolor="#FFFFFF", shape="box",
                   fillcolor="#000000", style="filled", xlabel="", labelfontsize="13.0")
            all_objs[tr] = this_uuid  # this_uuid
        elif tr.label not in trans_names:
            g.node(this_uuid, tr.label, shape="box", fontsize="13.0",
                   labelfontsize="13.0")
            trans_names[tr.label] = tr.label  # this_uuid
            all_objs[tr] = this_uuid
        else:
            all_objs[tr] = this_uuid

    for arc in obj.arcs:
        this_uuid = str(uuid.uuid4())

        if type(arc.source) == ObjectCentricPetriNet.Place:
            color = color_mapping[arc.source.object_type]
        if type(arc.target) == ObjectCentricPetriNet.Place:
            color = color_mapping[arc.target.object_type]

        if arc.variable == True:
            g.edge(all_objs[arc.source], all_objs[arc.target], label="",
                   color=color + ":white:" + color, fontsize="13.0")
        else:
            g.edge(all_objs[arc.source], all_objs[arc.target],
                   label="", color=color, fontsize="13.0")

        all_objs[arc] = this_uuid

    g.attr(overlap='false')
    g.attr(fontsize='11')

    g.format = image_format
    return g