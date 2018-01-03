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

def create_transcript_image(input_html):
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

        if image_type == 'middle':
            image_class = "tr_image_middle"
            figure_class = "figure_transcript_middle"
        elif image_type =="left":
            image_class = "tr_image_left"
            figure_class = "figure_transcript_left"
        elif image_type == 'not_set':
            image_class = "tr_image_middle"
            figure_class = "figure_transcript_middle"

        if img_tag.parent.name != 'a':
            bs_transcript = wrap_img(bs_transcript=bs_transcript, img_tag=img_tag,
                                     image_class=image_class, figure_class=figure_class)
        elif img_tag.parent.name == 'a':
            # 1. Refresh <a> link with ficaption
            # If figcaption was removed, add a new one
            figcaption_tag = img_tag.parent.parent.find("figcaption")
            if figcaption_tag is not None:
                new_img_desc = "".join((str(elem) for elem in figcaption_tag.contents))
            else:
                new_figcaption_tag = bs_transcript.new_tag("figcaption")
                img_tag.parent.insert_after(new_figcaption_tag)
                new_img_desc = ""
            img_tag.parent['title'] = new_img_desc

            # 2. check class and refresh based on longdescr

        else:
            pass
    return str(bs_transcript)
