var minWidescreen = 1920;
var maxMobile = 799;

$(function() {

    // Hamburger

    $(".hamburger")
        .click(function(event) {
            $( this ).toggleClass("is-active");
            if ( $( this ).is(".is-active") ) {
                $( "#menu" ).addClass('active');
                $( "header.site").addClass('menu-active');
                $( "body" ).css({'overflow:': 'hidden'})
                $( "img.hamburger" ).attr('src', "/static/img/menu-close.svg");
            } else {
                $( "img.hamburger" ).attr('src', "/static/img/menu-open.svg");
                $( "body" ).css({'overflow:': 'inherit'})
                $( "header.site").removeClass('menu-active');
                $( "#menu" ).removeClass('active');
            }
        });


    // Collapsed Sections

    $(".plugin h2.header button.collapse")
        .click(function(event) {
            $( this ).parentsUntil(".plugin").parent().toggleClass('collapsed');
            event.stopPropagation();
        });

    $(".menu button.collapse")
        .click(function(event) {
            $( this ).parentsUntil(".submenu").parent().toggleClass('collapsed');
            event.stopPropagation();
        });

    function scrollTo(element) {
        $('html, body').animate({
            scrollTop: $(element).offset().top
        }, 1000);
    }

    $("#read-more, #read-more-bottom")
        .click(function(event) {
            var button = $("#read-more"),
                bottom_button = $("#read-more-bottom"),
                target = $("#read-more-target");
            if (target.hasClass('collapsed')) {
                target.removeClass('collapsed');
                button.addClass('opened');
                button.data("text-original", button.text());
                button.text(button.data("text-open"));
                bottom_button.addClass('opened');
                bottom_button.data("text-original", bottom_button.text());
                bottom_button.text(bottom_button.data("text-open"));
                scrollTo(target);
            } else {
                target.addClass('collapsed');
                button.removeClass('opened');
                button.text(button.data("text-original"));
                bottom_button.removeClass('opened');
                bottom_button.text(bottom_button.data("text-original"));
                scrollTo($("#read-more"));
            }
        });


    // Make thumbnail boxes clickable

    $("a.box-link").each(
        function() {
            var $a = this;
            // $(this).parent().on({
            //     click: function(event) {
            //         $a.click();
            //         event.stopPropagation();
            //     }
            // });
            // FIXME Remove .thumbnail-box
            $(this).parents(".box, .thumbnail-box").addClass('clickable-box').click(function(event) {
                $a.click();
                event.stopPropagation();
            });
        }
    );


    // Make menu li boxes clickable

    $("body.frontpage ul.menu li a").each(
        function() {
            var $a = this;
            $(this).parent().click(function() {
                $a.click();
            });
        }
    );


    // Inline Slideshow

    function activateSlide(parent, slide_id) {
        var slide = parent.find("#" + slide_id);
        var dot = parent.find("a[data-target='#" + slide_id + "']");
        $(slide).siblings().removeClass('active');
        $(dot).siblings().removeClass('active');
        $(slide).addClass('active');
        $(dot).addClass('active');
    }

    function inlineSlideshowShiftThunbnails(slider) {
        var thumbs = slider.find('.thumbs-box')
        var active = thumbs.find('.active')
        if (active.length) {
            var offset = - active.position().left
            offset += thumbs.parent().width() / 2 - active.width() / 2
            thumbs.css({
                left: offset + 'px',
            })
        }
    }
    //FIXME: find better way to wait for layout to settle
    setTimeout(function() {
        $('.inline-slider').each(function(i, slider) {
            inlineSlideshowShiftThunbnails($(slider))
        })
    }, 1000)

    $('.inline-slider .thumbs a').click(function(event) {
        event.preventDefault();
        var parent = $(this).parents('.inline-slider');
        $(this).siblings().removeClass('active');
        $(this).addClass('active');
        parent.find($(this).data('target')).siblings().removeClass('active');
        parent.find($(this).data('target')).addClass('active');
        inlineSlideshowShiftThunbnails(parent)
    });

    $('.inline-slider .next').click(function(event) {
        event.preventDefault();
        var parent = $(this).parents('.inline-slider')
        var next = parent.find('.descendants li.active').next();
        if (next.length < 1) {
            next = parent.find('.descendants li').first();
        }
        activateSlide(parent, next.attr('id'));
        inlineSlideshowShiftThunbnails(parent)
    });

    $('.inline-slider .previous').click(function(event) {
        event.preventDefault();
        var parent = $(this).parents('.inline-slider')
        var prev = parent.find('.descendants li.active').prev();
        if (prev.length < 1) {
            prev = parent.find('.descendants li').last();
        }
        activateSlide(parent, prev.attr('id'));
        inlineSlideshowShiftThunbnails(parent)
    });


    // List / Search Filter Interaction

    $("button.reset").click(function(event) {
        $(".filters select").prop('selectedIndex', 0);
        // event.preventDefault();
    });

    $("label.filter").click(function(event) {
        if (event.altKey) {
            $input = $("#" + $(this).attr("for"));
            state = $input.prop("checked");
            $input.prop("checked", !state);
            $input.siblings("input[type=checkbox]").prop("checked", state);
            $(this).parents('form').submit();
        }
    });


    // Hide big scroll arrows on scroll

    $(window).scroll(function() {
        if ($(this).scrollTop() > 200) {
            $('nav.sibling').fadeOut(700);
        } else {
            $('nav.sibling').fadeIn(700);
        }
     });
});


// Archive navigation
document.querySelectorAll('nav.selection .header > a').forEach(function(a) {
    if (a.classList.contains('next') || a.classList.contains('previous')) {
        a.addEventListener('click', function(event) {
            event.preventDefault()
            var direction = a.classList.contains('next') ? 'next' : 'previous'
            slidePage(this.parentElement.parentElement, direction)
        })
    }
})

/*
// fails on firefox/android why?
$("nav.selection .descendants").on({
    'swipeleft': function(event) {
        var nav = $(this).parent('nav')[0],
            direction = 'next'
        if (! nav.classList.contains('descendants-fit-screen')) {
            slidePage(nav, direction)
        }
    },
    'swiperight': function(event) {
        var nav = $(this).parent('nav')[0],
            direction = 'previous'
        if (! nav.classList.contains('descendants-fit-screen')) {
            slidePage(nav, direction)
        }
    }
})
*/

function updateSelectionNavigation() {
    if ($(document).width() <= 799) {
        document.querySelectorAll('nav.selection.articles').forEach(function(selection) {
            repage(selection, 100)
        })
    }
    document.querySelectorAll('nav.selection').forEach(function(selection) {
        var pages_per_view = getPagesPerView(selection)
        var descendants = selection.querySelector('.descendants')
        if (descendants.querySelectorAll('.page').length) {
            selection.classList.add('first')
            descendants.querySelectorAll('.page').forEach(function(page) {
                page.classList.add('on')
            })
        }
        var width;
        if (descendants.querySelectorAll('.page').length <= pages_per_view) {
            selection.classList.add('descendants-fit-screen')
            width = ''
            setTimeout(function() {
                repage(selection, 100)
            })
        } else {
            selection.classList.remove('descendants-fit-screen')
            width = (descendants.querySelectorAll('.page').length * 100) + 'vw'
        }
        descendants.style.width = width
    })
}

updateSelectionNavigation()

function getPagesPerView(selection) {
    return 1
}

function slidePage(container, direction) {
    var pages_per_view = getPagesPerView(container)
    var descendants = container.querySelector('.descendants')
    var offset = parseInt(descendants.style.left || 0),
        max_offset = -(descendants.querySelectorAll('.page').length - 1)/pages_per_view * 100

    if (direction == 'next') {
        if (offset > max_offset) {
            offset -= 100
        }
    } else {
        offset += 100
        if (offset > 0) {
            offset = 0
        }
    }
    if (offset == max_offset) {
        container.classList.add('last')
    } else {
        container.classList.remove('last')
    }
    if (offset == 0) {
        container.classList.add('first')
    } else {
        container.classList.remove('first')
    }
    var padding = 10
    descendants.style.marginLeft = (padding * -offset / 100) + 'px'
    descendants.style.left = offset + 'vw'
}

function cyclePage(container, direction) {
    var old = $(container).find('.page.on'),
        current
    if (direction == 'next') {
        current = old.next()
        if (!current.length) {
            current = $(container).find('.page').first()
        }
    } else {
        current = old.prev()
        if (!current.length) {
            current = $(container).find('.page').last()
        }
    }
    current.addClass('on').removeClass('off')
    old.addClass('off').removeClass('on')

}

function cycleList(list, direction) {
    var ul = list.querySelector('.descendants')
    if (direction == 'next') {
        ul.appendChild(ul.firstElementChild)
    } else if (direction == 'previous') {
        ul.insertBefore(ul.lastElementChild, ul.firstElementChild)
    }
}

function repage(container, n) {
    var changed = false
    $(container).find('.page').each(function(i, page) {
        var next = $(page).next()[0],
            previous = $(page).prev()[0]
        while(page.children.length > n) {
            if (!next) {
                next = document.createElement('div')
                next.className = 'page on'
                page.parentElement.appendChild(next)
            }
            if (next.children.length) {
                next.insertBefore(page.children[page.children.length-1], next.firstElementChild)
            } else {
                next.appendChild(page.children[page.children.length-1])
            }
            changed = true
        }
        while(page.children.length < n && next && next.children.length) {
            page.appendChild(next.firstElementChild)
            changed = true

        }
        if (!page.children.length) {
            page.remove()
        }
    })
    if (changed) {
        return repage(container, n)
    } else {
        return changed
    }
}


function repageSelections() {
    var n = $(document).width() >= minWidescreen ? 8 : 4
    var pages_per_view = 1
    $("nav.related-articles, nav.articles, nav.itembundles").each(function(i, element) {
        repage(element, n)

        var descendants = element.querySelector('.descendants')
        descendants.style.left = '0'
        element.classList.remove('last')
        element.classList.remove('first')
        if (descendants.querySelectorAll('.page').length) {
            element.classList.add('first')
            descendants.querySelectorAll('.page').forEach(function(page) {
                page.classList.add('on')
            })
        }
        var width;
        if (descendants.querySelectorAll('.page').length <= pages_per_view) {
            element.classList.add('descendants-fit-screen')
            width = ''
            setTimeout(function() {
                repage(element, 100)
            })
        } else {
            element.classList.remove('descendants-fit-screen')
            width = (descendants.querySelectorAll('.page').length * 100) + 'vw'
        }
        descendants.style.width = width
    })
}

function repagePeople() {
    var n = $(document).width() <= maxMobile ? 4 : 5
    n = $(document).width() >= minWidescreen ? 10 : n
    var pages_per_view = 1
    $("nav.selection.team, nav.selection.actors").each(function(i, element) {
        repage(element, n)

        var descendants = element.querySelector('.descendants')
        descendants.style.left = '0'
        element.classList.remove('last')
        element.classList.remove('first')
        if (descendants.querySelectorAll('.page').length) {
            element.classList.add('first')
            descendants.querySelectorAll('.page').forEach(function(page) {
                page.classList.add('on')
            })
        }
        var width;
        if (descendants.querySelectorAll('.page').length <= pages_per_view) {
            element.classList.add('descendants-fit-screen')
            width = ''
            setTimeout(function() {
                repage(element, 100)
            })
        } else {
            element.classList.remove('descendants-fit-screen')
            width = (descendants.querySelectorAll('.page').length * 100) + 'vw'
        }
        descendants.style.width = width
    })
}
function repageOnResize() {
    repageSelections()
    repagePeople()
}

$(window).on({
    resize: repageOnResize
})
repageOnResize()

// Gallery Navigation
//$(function() {
    var languageSVG = ($('.language-selector a[hreflang="en"]').html() || '').replace('EN', '??')
    var step_class = '.player-controls-step'
    var slide, step, isFullscreen = false

    slide = document.querySelector('.slide.active')
    if (!slide) {
        slide = document.querySelector('.slide')
    }
    step = document.querySelector(step_class + '.current')
    if (!step) {
        step = document.querySelector(step_class)
    }
    if (slide && step) {
        slide.classList.add('active')
        step.classList.add('current')

        document.querySelectorAll('#player-controls button').forEach(function(element) {
            if (element.classList.contains('previous')) {
                element.addEventListener('click', function(event) { previous() })
            } else if (element.classList.contains('next')) {
                element.addEventListener('click', function(event) { next() })
            } else if (element.classList.contains('fullscreen')) {
                element.addEventListener('click', function(event) {
                    enterFullscreen()
                })
            }
        })
        $('.stage figure img').on({click: function() {
            if (isFullscreen) {
                exitFullscreen()
            } else {
                enterFullscreen()
            }
        }})

        document.querySelectorAll('.thumbs a').forEach(function(element) {
            element.addEventListener('click', function(event) {
                if (this.attributes.href.value[0] == '#') {
                    updateSelected(this.parentElement)
                    var step = document.querySelector(this.attributes.href.value)
                    if (step && step.classList.contains(step_class.slice(1))) {
                        setCurrentStep(step)
                        event.preventDefault()
                    }
                }
            })
        })
        updatePosition()
        if (document.querySelector('#stage-text .inscription-text')) {
            var switch_type = document.querySelector('.right-button-group button.type-switch')
            switch_type.style.display = 'inline-block'
            switch_type.addEventListener('click', function(event) {
                toggleType(switch_type)
            })

        }
    } else if (document.querySelector('#stage-text .inscription-text')) {
        updateStageTextLanguageIcon()
        updateStageIcon()
        document.querySelector('#player-controls button.fullscreen').style.display = 'inline-block'
        document.querySelectorAll('#player-controls button.fullscreen').forEach(function(element) {
            if (element.classList.contains('fullscreen')) {
                element.addEventListener('click', function(event) { enterFullscreen() })
            }
        })
    }

    /*
    window.addEventListener('hashchange', hashchange);
    hashchange()

    function hashchange() {
        if (document.location.hash.length > 1) {
            var step = document.querySelector(document.location.hash)
            if (step && step.classList.contains(step_class.slice(1))) {
                setCurrentStep(step)
            }
        }
    }
    */


    function getSlide(element) {
        if (element.classList.contains('slide')) {
            return element
        } else {
            return getSlide(element.parentElement)
        }
    }

    function selectStep(id) {
        var step_  = document.querySelector(id)
        setCurrentStep(step_)
    }

    function setCurrentStep(current) {
        step = current
        slide = getSlide(step)
        if (step.id) {
            var thumblink = document.querySelector('.thumbs .' + step.id)
            if (thumblink && thumblink.attributes.href.value[0] != '#') {
                document.location.href = thumblink.href
                return
            }
        }
        if (!slide.classList.contains('active')) {
            document.querySelectorAll('.active').forEach(function(element) {
                element.classList.remove('active')
            })
            slide.classList.add('active')
        }
        if (!step.classList.contains('current')) {
            document.querySelectorAll(step_class + '.current').forEach(function(element) {
                element.classList.remove('current')
            })
            step.classList.add('current')
        }
        updatePosition()
        updateCaption()

        if (thumblink) {
            updateSelected(thumblink.parentElement)
        }
    }

    function previous() {
        var current,
            previous,
            elements = document.querySelectorAll(step_class);

        elements.forEach(function(element) {
            if (!current && element.classList.contains('current')) {
                current = element
            }
            if (!current) {
                previous = element
            }
        })
        if (!previous) {
            previous = elements[elements.length-1]
        }
        setCurrentStep(previous)
    }

    function next() {
        var current,
            next,
            elements = document.querySelectorAll(step_class);

        elements.forEach(function(element) {
            if (!current && element.classList.contains('current')) {
                current = element;
            } else if (current && !next) {
                next = element;
            }
        })
        if (!next) {
            next = elements[0]
        }
        setCurrentStep(next)
    }

    function updateSelected(selected) {
        document.querySelectorAll('.thumbs li.selected').forEach(function(li) {
            if (li != selected) {
                li.classList.remove('selected')
            }
        })
        selected.classList.add('selected')
        document.querySelectorAll('.thumbs li.active').forEach(function(li) {
            li.classList.remove('active')
        })
        if (selected.nextElementSibling) {
            selected.nextElementSibling.classList.add('active')
        } else if (selected.previousElementSibling && selected.previousElementSibling.previousElementSibling) {
            selected.previousElementSibling.previousElementSibling.classList.add('active')
        }
        if (selected.previousElementSibling) {
            selected.previousElementSibling.classList.add('active')
        } else if (selected.nextElementSibling && selected.nextElementSibling.nextElementSibling) {
            selected.nextElementSibling.nextElementSibling.classList.add('active')
        }
    }

    function updatePosition() {
        var position=0
        if (step) {
            document.querySelectorAll(step_class).forEach(function(element) {
                position++
                if (element == step) {
                    document.querySelector('#gallery-navigation-controls .current').innerText = position
                }
            })
            document.querySelector('#gallery-navigation-controls .total').innerText = position
        }
        if (position) {
            document.querySelector('#player-controls button.fullscreen').style.display = 'inline-block'
        }
        if (position > 1) {
            document.querySelector('#gallery-navigation-controls').style.display = 'flex'
            $('.stage .thumbs').show()
        } else {
            //document.querySelector('#gallery-navigation-controls').style.display = 'none'
            $('.stage .thumbs').hide()
        }
        updateStageIcon()
        //updateLanguageIcon()
    }

    function updateStageIcon() {
        var html = ''
        if (slide) {
            var type = slide.dataset.type
            if (type) {
                html = '<img src="/static/img/' + type + '.svg">'
            }
        } else if (document.querySelector('#stage-text .inscription-text.active')) {
            html = '<img src="/static/img/text.svg">'
        }
        var icon = document.querySelector('#player-controls .stage-icon')
        if (icon && icon.innerHTML != html) {
            icon.innerHTML = html
        }
        var audio_display = ''
        if (document.querySelectorAll('.playlist .selected > a').length
                && document.querySelectorAll('.itembundle.faksimile').length) {
            audio_display = 'inline-block'
        }
        var audio_icon = document.querySelector('#player-controls .audio-player-start-icon')
        if (audio_icon) {
            audio_icon.style.display = audio_display
        }
    }

    function updateLanguageIcon() {
        var selected = document.querySelector('.playlist .selected > a')
        if (selected) {
            var language = selected.dataset.language
            var stage_language_switcher = document.querySelector('.stage-language-switcher')
            if (language) {
                stage_language_switcher.style.display = 'inline-block'
                updateTspan(stage_language_switcher.querySelector('#language tspan'), language)
                stage_language_switcher.querySelector('.language-switcher').replaceWith(
                    document.querySelector('.playlist-item .language-switcher').cloneNode(true)
                )
                addLanguageSwitcherEvents(stage_language_switcher)
                addLanguageSwitcherLinkEvents(stage_language_switcher)
            } else {
                stage_language_switcher.style.display = 'none'
            }
        }
    }


    // TEXT

    function buildLanguageSwitcher(items) {
        var switcher = document.createElement('div')
        switcher.classList.add('language-switcher')
        var selector = document.createElement('ul')
        selector.classList.add('language-selector')
        items.forEach(function(item) {
            var li = document.createElement('li')
            var a = document.createElement('a')
            a.href = '#'
            a.title = item.language
            if (item.code == 'ROM') {
                a.innerHTML = languageSVG.replace('??', item.code || '??').replace('16.7739', '9')
            } else {
                a.innerHTML = languageSVG.replace('??', item.code || '??')
            }


            a.onclick = function(event) {
                event.preventDefault()
                $('#stage-text .inscription-text.active').removeClass('active')
                item.item.classList.add('active')
                switcher.parentElement.querySelectorAll(
                    '.current-language'
                ).forEach(function(e) {
                    updateTspan(e.querySelector('#language tspan'), item.code)
                })
            }
            li.appendChild(a)
            selector.appendChild(li)
        })
        switcher.appendChild(selector)
        return switcher
    }

    function updateTspan(tspan, code) {
        tspan.innerHTML = code
        tspan.setAttribute('x', code == 'ROM' ? '9' : '16.7739')
    }
    function updateStageTextLanguageIcon() {
        var items = []
        document.querySelectorAll('#stage-text .inscription-text').forEach(function(text) {
            items.push({
                code: text.dataset.code,
                language: text.dataset.language,
                item: text
            })

        })

        if (items.length) {
            var active = document.querySelector('#stage-text .inscription-text.active')
            if (!active) {
                active = items[0].item
                active.classList.add('active')
            }
            language = active.dataset.code
            var stage_language_switcher = document.querySelector('.stage-language-switcher')
            if (language && items.length > 1) {
                stage_language_switcher.style.display = 'inline-block'
                updateTspan(stage_language_switcher.querySelector('#language tspan'), language)
                stage_language_switcher.querySelector('.language-switcher').replaceWith(
                    buildLanguageSwitcher(items)
                )
                addLanguageSwitcherEvents(stage_language_switcher)
                addLanguageSwitcherLinkEvents(stage_language_switcher)
            } else {
                stage_language_switcher.style.display = 'none'
                updateStageIcon()
            }
        }
    }
    function toggleType(switch_type) {
        var stage_icon = document.querySelector('#player-controls .stage-icon')
        stage_icon.firstChild.src = switch_type.firstChild.src
        if (switch_type.firstChild.attributes.src.value == '/static/img/text.svg') {
            switch_type.firstChild.src = '/static/img/faksimile.svg'
            document.querySelectorAll('.stage .slide, #gallery-navigation-controls').forEach(function(active) {
                active.style.display = 'none'
            })
            updateStageTextLanguageIcon()
        } else {
            switch_type.firstChild.src = '/static/img/text.svg'
            document.querySelectorAll('#stage-text .inscription-text.active').forEach(function(active) {
                active.classList.remove('active')
            })
            document.querySelectorAll('.stage .slide, #gallery-navigation-controls').forEach(function(active) {
                active.style.display = ''
            })
            updatePosition()
            var stage_language_switcher = document.querySelector('.stage-language-switcher')
            stage_language_switcher.style.display = 'none'
        }
    }

    function updateCaption(item) {
        item = item || step
        if (item) {
            var caption = item.querySelector('.caption')
            var creditLine = item.querySelector('.credit-line')
            document.querySelector('section.caption .caption').innerHTML = caption ? caption.innerHTML : ''
            document.querySelector('section.caption .credit-line').innerHTML = creditLine ? creditLine.innerHTML : ''
        }
    }

    $('button.fullscreen').on({
        click: function(event) {
            var parent = $(this).parents('figure')
            if (parent.length) {
                event.stopPropagation()
                enterFullscreen(parent[0])
            }
        }
    })

    function enterFullscreen(element) {
        if (!element && slide && slide.style.display == 'none') {
            element = document.querySelector('.stage .inscription-text.active')
        }
        element = element || slide || document.querySelector('.stage .active')
        if (!document.fullscreenElement &&
            !document.msFullscreenElement &&
            !document.mozFullScreenElement &&
            !document.webkitFullscreenElement) {
            if (element.requestFullscreen) {
                element.requestFullscreen();
            } else if (element.msRequestFullscreen) {
                element.msRequestFullscreen();
            } else if (element.mozRequestFullScreen) {
                element.mozRequestFullScreen();
            } else if (element.webkitRequestFullscreen) {
                element.webkitRequestFullscreen();
            }
        }
        var exit = document.createElement('nav')
        exit.id = 'fullscreen-controls'
        var button = document.createElement('button')
        button.innerHTML = '<img src="/static/img/full-screen-exit.svg">'
        button.onclick = function() {
            exitFullscreen(element)
        }
        exit.appendChild(button)
        element.appendChild(exit)
        isFullscreen = true
    }

    function exitFullscreen(element) {
        element = element || slide
        if (document.exitFullscreen) {
            document.exitFullscreen();
        } else if (document.msExitFullscreen) {
            document.msExitFullscreen();
        }else if (document.mozCancelFullScreen) {
            document.mozCancelFullScreen();
        }else if (document.webkitCancelFullScreen) {
            document.webkitCancelFullScreen();
        }
        element.querySelectorAll('#fullscreen-controls').forEach(function(control) {
            element.removeChild(control)
        })
        isFullscreen = false
    }
//})


// Playlist Controller
//$(function() {
    document.querySelectorAll('.playlist-item .play-button').forEach(function(element) {
        element.addEventListener('click', function(event) {
            var item = this.parentElement
            selectPlaylistItem(item)

        })
    })
    document.querySelectorAll('.playlist-item a.playlist-src').forEach(function(element) {
        element.addEventListener('click', function(event) {
            event.preventDefault()
            var item = getPlaylistItem(this)
            var language = this.dataset.language
            var duration = this.dataset.duration
            selectPlaylistItem(item, language, duration)
        })
    })
    document.querySelectorAll('#player-controls .audio-player-start-icon').forEach(function(element) {
        element.addEventListener('click', function(event) {
            document.querySelector('.playlist .selected > a').click()
        })
    })
    document.querySelectorAll('.current-language').forEach(function(element) {
        element.addEventListener('click', function(event) {
            var switcher = this.parentElement.querySelector('.language-switcher')
            if (this.classList.contains('open')) {
                this.classList.remove('open')
                switcher.classList.remove('open')
            } else {
                this.classList.add('open')
                switcher.classList.add('open')
            }
        })
    })

    addLanguageSwitcherEvents(document)


    function addLanguageSwitcherLinkEvents(base) {
        base.querySelectorAll('a.playlist-src').forEach(function(element) {
            element.addEventListener('click', function(event) {
                event.preventDefault()
                var item = getPlaylistItem(this)
                var language = this.dataset.language
                var duration = this.dataset.duration
                selectPlaylistItem(item, language, duration)
            })
        })
    }
    function addLanguageSwitcherEvents(base) {
        base.querySelectorAll('.language-switcher').forEach(function(element) {
            element.addEventListener('click', function(event) {
                if (this.classList.contains('open')) {
                    this.classList.remove('open')
                    document.querySelectorAll('.current-language.open').forEach(function(element) {
                        element.classList.remove('open')
                    })
                }
            })
        })
    }


    function getPlaylistItem(element) {
        if (!element) {
            return document.querySelector('.playlist-item.selected')
        }
        else if (element.classList.contains('playlist-item')) {
            return element
        }
        return getPlaylistItem(element.parentElement)
    }

    function updateSelectedSource(href) {
        document.querySelectorAll('.playlist-src').forEach(function(element) {
            if (element.href == href) {
                element.parentElement.classList.add('selected')
            }  else if (element.parentElement.classList.contains('selected')) {
                element.parentElement.classList.remove('selected')
            }
        })
    }

    function selectPlaylistItem(item, language, duration) {
        var src
        document.querySelectorAll('.current-language.open, .language-switcher.open').forEach(function(element) {
            element.classList.remove('open')
        })
        if (language) {
            src = item.querySelector('.playlist-src[data-language=' + language + ']')
        } else {
            src = item.querySelector('li.selected .playlist-src')
            if (!src) {
                src = item.querySelector('.playlist-src')
            }
        }

        var type = item.dataset.type
        var player = document.querySelector('#playlist-mediaplayer')

        if (type == 'audio') {
            var audio = player.querySelector('audio')
            if (!audio) {
                audio = document.createElement('audio')
                audio.controlls = true
                player.appendChild(audio)
            }
            if (audio.src != src.href) {
                audio.src = src.href
                audio.play()
                updateSelectedSource(src.href)
            } else {
                if (audio.paused) {
                    audio.play()
                } else {
                    audio.pause()
                }
            }
            document.querySelectorAll('.playlist-item.selected .play-button').forEach(function(element) {
                element.innerHTML = audio.paused
                    ? '<img src="/static/img/playlist-play.svg">'
                    : '<img src="/static/img/playlist-pause.svg">'
                element.title = element.dataset[audio.paused ? 'play' : 'pause']
            })
            document.querySelectorAll('.playlist-item .play-button').forEach(function(element) {
                if (!element.parentElement.classList.contains('selected')) {
                    element.innerHTML = '<img src="/static/img/playlist-play.svg">'
                    element.title = element.dataset.play
                }
            })
        } else if (type == 'iframe') {
            var iframe = player.querySelector('iframe')
            if (!iframe) {
                iframe = document.createElement('iframe')
                iframe.allowfullscreen = true
                player.appendChild(iframe)
            }
            if (iframe.src != src.href) {
                iframe.src = src.href
                updateSelectedSource(src.href)
            } else {
                //console.log('same item', src.href)
            }
        }
        if (!language) {
            language = src.dataset.language
        }
        document.querySelectorAll(
            '.current-language'
        ).forEach(function(switcher) {
            if (switcher) {
                if (language) {
                    switcher.style.display = 'inline-block'
                    updateTspan(switcher.querySelector('#language tspan'), language)
                } else {
                    switcher.style.display = 'none'
                }
            }
        })

        var active_slide = document.querySelector('.slide.active')
        if (active_slide && active_slide.dataset.type == type) {
            updateCaption(item)
        }

        if (duration) {
            item.querySelector('.duration-var').innerText = duration
        }
    }

    // Swap Play Controls Position for Mobile View

    function movePlayerControls() {
        var head = document.querySelector('.head')
        var stage = document.querySelector('div.stage')
        var controls = document.querySelector('#player-controls')
        if (controls) {
            if ($(document).width() <= 799) {
                head.appendChild(controls)
            } else {
                head = document.querySelector('header.article .info')
                head.appendChild(controls)
            }
        }
    }
    $(window).on({resize: movePlayerControls})
    movePlayerControls()

//})



// special links
document.querySelectorAll('.plugin.speciallink').forEach(function(element) {
    var a = element.querySelector('.plugin-content a')
    if (a) {
        element.querySelectorAll('a.go-to').forEach(function(go) {
            go.href = a.href
        })
    }
})


//
// Frontpage

if (window.intro_slides) {
    var speed = 1000
    var intro_steps = []
    var side = 'left', type = 'image', position = 0
    intro_slides.forEach(function(slide) {
        [1, 2].forEach(function() {
            intro_steps.push({
                'type': type,
                'color': slide.color,
                'content': type == 'text' ? slide.text : slide.image_html,
                'url': slide.url
            })
            type = type == 'text' ? 'image' : 'text'
        })
    })

    document.querySelectorAll('.intro-slide .image').forEach(function(image) {
        image.addEventListener('click', function(event) {
            document.location.href = intro_steps[0].url
        })
    })

    side = 'left'
    position = 2
    function nextIntroSlide() {
        var t0 = +new Date
        var step = intro_steps[position]
        var side = [1, 2].indexOf(position % 4) > -1 ? 'left' : 'right'
        var slide = document.querySelector('.intro-slide .' + side)
        position++
        if (position >= intro_steps.length) {
            position = 0
        }
        var active = slide.querySelector('.active')
        var next = document.createElement('div')
        next.classList.add('next')
        next.classList.add(step.type)
        next.innerHTML = step.content
        if (step.type == 'text') {
            next.style.backgroundColor = step.color
        } else {
            next.style.backgroundColor = '#000'
            next.addEventListener('click', function(event) {
                document.location.href = step.url
            })
        }
        slide.appendChild(next)
        next.style.zIndex = 1
        active.style.zIndex = 0

        function show() {
            next.classList.add('active')
            setTimeout(function() {
                active.parentElement.removeChild(active)
                next.classList.remove('next')
                setTimeout(nextIntroSlide, 1000)
            }, 1000)
        }

        var img = next.querySelector('img')
        if (img) {
            img.onload = function() {
                var delay = +new Date - t0
                setTimeout(show, speed-delay)
            }
        } else {
            setTimeout(show, speed)
        }
    }
    intro_steps.length && setTimeout(nextIntroSlide, speed)
}


// curatorial content
$('.plugin.header-background video').on({
    ended: function() {
        $('.plugin.header-background button.play').show()
    }
})
$('.plugin.header-background button.video.play').on({
    click: function() {
        $('.plugin.header-background button.play').hide()
        $('.plugin.header-background video')[0].play()
    }
})

// faksimile player
$('.plugin.header-background audio').on({
    ended: function() {
        $('.plugin.header-background button.play').show()
        $('.plugin.header-background button.pause').hide()
    }
})
$('.plugin.header-background video').on({
    ended: function() {
        $('.plugin.header-background button.play').show()
    }
})
$('.plugin.header-background button.audio').on({
    click: function() {
        var audio = $('.plugin.header-background audio')[0]
        if (audio && audio.paused) {
            $('.plugin.header-background button.play').hide()
            $('.plugin.header-background button.pause').show()
            audio.play()
        } else {
            $('.plugin.header-background button.pause').hide()
            $('.plugin.header-background button.play').show()
            audio.pause()
        }
    }
})

if($('.stage .document').length) {
    $(document).on({
        keydown: function(event) {
            if (fullScreen) {
                if (event.key == 'ArrowRight') {
                    next();
                } else if (event.key == 'ArrowLeft') {
                    previous();
                }
            }
        }
    })
}
