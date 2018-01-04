import bs4 as bs

def _wrap(to_wrap, wrap_in):
    contents = to_wrap.replace_with(wrap_in)
    wrap_in.append(contents)


def wrap_img(bs_transcript, img_tag, image_class, figure_class):
    """
    Wrap <img> tag based on class info.

    Parameters
    ----------
    bs_transcript: BeautifulSoup (bs4) object
    img_tag: bs4 image tag
    image_class, figure_class: str
        classes for the img and figure tags
    """
    img_src = img_tag.attrs['src']

    if img_tag.has_attr("title"):
        img_desc = img_tag.attrs['title']
    else:
        img_desc = ""

    img_tag.attrs['class'] = image_class
    img_tag.attrs['style'] = ""
    new_figure_tag = bs_transcript.new_tag("figure", **{'class': figure_class})
    new_anchor_tag = bs_transcript.new_tag("a", **{'class':'fancybox_transcript', 'href': img_src,
                                                   'title': img_desc})

    new_figcaption_tag = bs_transcript.new_tag("figcaption")
    new_figcaption_tag.string = img_desc
    _wrap(img_tag, new_figure_tag)
    img_tag.insert_after(new_figcaption_tag)
    _wrap(img_tag, new_anchor_tag)
    return bs_transcript

def parse_double(bs_transcript):
    """
    Parse BeautifulSoup object bs_transcript: if there are 2 'double' <figure> tags
    then wrap them in a column and row div

    Parameters
    ----------
    bs_transcript: BeautifulSoup object

    Returns
    -------
    bs_transcript: BeautifulSoup object
    """
    for idx, figure_tag in enumerate(bs_transcript.findAll('figure', {'class': 'figure_transcript_double'})):
        next_figure_tag = figure_tag.find_next_sibling()
        if next_figure_tag is None:
            continue

        if (next_figure_tag.name=='figure') & (next_figure_tag.get('class', '')=='figure_transcript_double'):
            col_div = bs_transcript.new_tag("div", **{'class': 'col-md-6'})
            _wrap(to_wrap=figure_tag, wrap_in=col_div)
            col_div = bs_transcript.new_tag("div", **{'class': 'col-md-6'})
            _wrap(to_wrap=next_figure_tag, wrap_in=col_div)

            # add a row div around both column divs
            new_row = bs_transcript.new_tag('div', **{'class':'row'})
            figure_tag.parent.insert_before(new_row)

            new_row.append(figure_tag.parent)
            new_row.append(next_figure_tag.parent)
        else:
            print("wrong div! with index: {}".format(idx))
            pass
    return bs_transcript



def style_transcript_image(input_html):
    """
    Take transcript and check if any of the images have a 'le_image_middle' or
    'le_image_left' as one of their classes. If so, wrap them in the correct tags.

    Parameters
    ---------
    input_html: str
        Transcript as html

    Returns
    -------
    New html transcript as a string
    """
    bs_transcript = bs.BeautifulSoup(input_html, 'html.parser')

    for img_tag in bs_transcript.findAll("img"):

        if img_tag.has_attr("longdesc"):
            image_type = img_tag['longdesc']
        else:
            image_type = 'not_set'

        if image_type =="left":
            image_class = "tr_image_left"
            figure_class = "figure_transcript_left"
        elif image_type == "double":
            image_class = "tr_image_double"
            figure_class = "figure_transcript_double"
        # default is 'middle'
        else:
            image_class = "tr_image_middle"
            figure_class = "figure_transcript_middle"

        if img_tag.parent.name != 'a':
            bs_transcript = wrap_img(bs_transcript=bs_transcript, img_tag=img_tag,
                                     image_class=image_class, figure_class=figure_class)
        elif img_tag.parent.name == 'a':
            # 1. Refresh <a> link with ficaption
            figcaption_tag = img_tag.parent.parent.find("figcaption")
            # If figcaption was removed, add a new one
            if figcaption_tag is not None:
                new_img_desc = "".join((str(elem) for elem in figcaption_tag.contents))
            else:
                new_figcaption_tag = bs_transcript.new_tag("figcaption")
                img_tag.parent.insert_after(new_figcaption_tag)
                new_img_desc = ""
            img_tag.parent['title'] = new_img_desc

            # 2. Refresh <img> and <figcaption> classes
            img_tag['class'] = image_class
            img_tag.parent.parent['class'] = figure_class
        else:
            pass
    bs_transcript = parse_double(bs_transcript)
    return str(bs_transcript)
