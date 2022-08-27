/*global $, ICMLocale, ICMBranchID, Blinger, Cookies, zE*/
var domain = '.icmarkets.com';

function getSignTokenCommon() {
  var $def = $.Deferred();
  $.get(window['serverURL'] + '~get~sign~token~?nocache=' + Date.now()).done(function (token) {
    $def.resolve(token);
  }).fail(function () {
    $def.resolve(null);
  });
  return $def.promise();
}

function saveCampClick(camp) {
  camp = camp.replace(/\D/g, ''); // strip non-digits
  getSignTokenCommon().then(function(token) {
    var query = '?getAction=camp_click&data=' + camp;
    var uri = window['serverURL'] + query + '&sign=' + token;
    $.ajax({
      dataType: "json",
      url: uri
    });
  });
}

if (window && window.location) {
    domain = window.location.hostname.replace('www.', '.');
    if (domain.indexOf('.') !== 0) {
        domain = '.' + domain;
    }
}
if (domain.indexOf('localhost') !== -1) domain = 'localhost';
if (Cookies.get('camp_click')) {

    saveCampClick(Cookies.get('camp_click'));
    Cookies.set('camp_click', '', {expires: -1, domain: domain});
}

function isMobile() {
  try {
    document.createEvent("TouchEvent");
    return true;
  }
  catch (e) {
    return false;
  }
}

if (window['enableLivechat']) {
    $('.goto-support').hide();

    if (ICMLocale === 'cn') {
        $('.icm-messengers-links a').on('click', function (event) {
            if (event.target.href) {
                event.preventDefault();
                window.open(event.target.href, "_blank", "width=500,height=700");
            }
        })
    } else if (isMobile()) {
        // load and show BLINGER only
        $('html').toggleClass('desktop-pc', false);
        $('html').toggleClass('touch-device', true);

        // eslint-disable-next-line no-unused-vars
        var customBlingerConfig = { settings: {showPowered: false }};

        (function (d) {var s = d.createElement("script");s.async = true;s.charset = "utf-8";s.src = "https://app.blinger.io/uploads/widgets2/523.js";d.head.appendChild(s);}(window.document));

        // eslint-disable-next-line func-style
        var showBlinger = function () {
            if (typeof Blinger !== 'undefined' && !Blinger.launcherWidget.isOpen) {
                document.getElementById('blinger-launcher-iframe').style.display = 'block';
            }
        };
        window.zESettings = {
            webWidget: {
                offset: {
                    horizontal: '100px'
                },
            },
        };

        // eslint-disable-next-line func-style
        window['blingerBeforeRender'] = function () {
            var channel = new Blinger.Channels.SimpleActionChannel();
            channel.tooltip = 'LiveChat';
            channel.color = 'orange';
            channel.backgroundColor = 'orange';
            channel.imageUrl = 'https://app.blinger.io/images/widget2/livechat.png';
            channel.action = function () {
                zE('webWidget', 'show');
                zE('webWidget', 'open');
            };

            Blinger.channelsWidget.addChannel(channel);
            Blinger.channelsWidget.resizeEnabled = true;
        };
        // eslint-disable-next-line func-style
        window['blingerInit'] = function () {
            document.getElementById('blinger-launcher-iframe').style.display = 'none';
        };

        // eslint-disable-next-line block-scoped-var
        let $s = document.createElement('script');
        // eslint-disable-next-line block-scoped-var
        let el = document.getElementsByTagName('script')[0];
        // eslint-disable-next-line block-scoped-var
        $s.async = !0;
        // eslint-disable-next-line block-scoped-var
        $s.setAttribute('charset','utf-8');
        // eslint-disable-next-line block-scoped-var
        $s.id = 'ze-snippet';
        // eslint-disable-next-line block-scoped-var
        $s.src = '';
        switch (ICMBranchID) {
            case "4": // BS (SCB)
                // $s.src = 'https://static.zdassets.com/ekr/snippet.js?key=e21062f0-1797-4f3a-940c-71d98b2ecda7';
                // break;
            // eslint-disable-next-line no-fallthrough
            case "3": // SC (FSA)
                $s.src = 'https://static.zdassets.com/ekr/snippet.js?key=e21062f0-1797-4f3a-940c-71d98b2ecda7';
                break;
            case "2": // EU (CySEC)
                $s.src = 'https://static.zdassets.com/ekr/snippet.js?key=627ffd23-89f6-4fce-b0cc-12d2fddb4cab';
                break;
            case "1": // AU (ASIC)
            default:
                $s.src = 'https://static.zdassets.com/ekr/snippet.js?key=d264e4de-bd01-4bf9-b215-770553a2ebaa';
        }
        $s.type = 'text/javascript';
        $s.onload = function () {
            var checkZeInstanceInterval = setInterval(function () {
                if (typeof window.zE != 'undefined') {
                    clearInterval(checkZeInstanceInterval);
                    zE('webWidget:on', 'close', function() {
                        zE('webWidget', 'hide');
                    });
                    operateWithZE();
                }
            }, 100);
        };
        el.parentNode.insertBefore($s, el);
        // eslint-disable-next-line no-inner-declarations
        function operateWithZE () {
            var checkZeLauncherInterval = setInterval(function () {
                let zEwidgetDisplay = zE('webWidget:get', 'display');
                if (zEwidgetDisplay === 'launcher') {
                    clearInterval(checkZeLauncherInterval);
                    showBlinger();
                }
            }, 100);
        }
    } else {
        // load and show LIVECHAT only
        $('html').toggleClass('desktop-pc', true);
        $('html').toggleClass('touch-device', false);
    }
} else {
    $('.goto-support').show();
}

// function createPerfectLauncherButtonForDesktopChat () {
//     var $container = $('<div class="launcher-button-container"></div>');
//     var $wrap = $('<div class="launcher-button-wrapper"></div>');
//     var $button = $('<a id="launcher-button" href="#" class="launcher-button"></a>');
//     var $rings = $('<div id="rings" class="rings" style="display: block;"></div>');
//     var $ring = $('<div class="ring" style="border-color: #08ba2f"></div>');
//     $rings.append($ring).append($ring).append($ring);
//     $button.append($rings);
//     $wrap.append($button);
//     $container.append($wrap);
//
//     $button.on('click', function () {
//         window.zE('webWidget', 'open');
//         $container.toggleClass('show', false);
//     });
//
//     // $zopim.livechat.button.hide();
//
//     window.zE('webWidget:on', 'open', function () {
//         $container.toggleClass('show', false);
//     })
//     window.zE('webWidget:on', 'close', function () {
//         $container.toggleClass('show', true);
//     })
//
//     $('body').append($container);
//     $container.toggleClass('show', true);
// }

$('.page-header__menu-container .menu-switch').on('click', function() {
  $(this).parents('.page-header__menu-container').toggleClass('expanded');
});

$('.sidebar-cta-card-container.random-background').each(function() {
  $(this).addClass('rnd-back-' + (Math.floor(Math.random() * (3 - 1 + 1)) + 1));
});


// eslint-disable-next-line no-unused-vars
function openLiveChat(forced) {
    if (window.openChatWidget) window.openChatWidget() // open chat dialog if current page is help-centre (widget only there)
    else window.location = window['helpCentreLink'];   // redirect to help-centre page where chat dialog will present
}

$('.spreads-block__expand-button').on('click', function () {
    var $button = $(this);
    var $panel = $(this).parent().find('.panel-collapse');
    var isCollapsed = $button.is('.collapsed');
    $button.toggleClass('collapsed', !isCollapsed);
    $panel.toggleClass('in', isCollapsed);
});

$('.spreads-block').on('click', '.skin-toggle', function () {
    var $button = $(this);
    var $panel = $(this).closest('.panel-collapse');
    var $table = $panel.find('.single-design-table');
    var switchSkinTo = ($button.is('.skin-light') ? 'light-skin' : 'dark-skin');
    $table.toggleClass('light-skin', false).toggleClass('dark-skin', false).toggleClass(switchSkinTo, true);
});

$('.spreads-block input.spreads-search-box').on('input', function () {
    var $input = $(this);
    var value = $input.val();
    var $panel = $(this).closest('.panel-collapse');
    $panel.find(".symbol-group-toggle").toggleClass('symbol-group-active', false);
    var $table = $panel.find('.single-design-table');
    var $row = $table.find('.table-row');
    $row.show();
    if (value && value.length) {
        $row.each(function () {
            var $currentRow = $(this);
            var $nameCell = $currentRow.find('.table-cell.c1');
            var name = $nameCell.text();
            if (name && name.toUpperCase().indexOf(value.toUpperCase()) === -1) {
                $currentRow.hide();
            }
        });
    }
});

$('.spreads-block').on('click', '.symbol-group-toggle', function () {
    $(".symbol-group-toggle").toggleClass('symbol-group-active', false);
    var $selectedGroupTab = $(this);
    $selectedGroupTab.toggleClass('symbol-group-active', true);
    var selectedGroup = $selectedGroupTab.text();
    var $panel = $(this).closest('.panel-collapse');
    var $table = $panel.find('.single-design-table');
    var $row = $table.find('.table-row');
    $row.show();
    if (selectedGroup) {
        $row.each(function () {
            var $currentRow = $(this);
            var $symbolGroupCell = $currentRow.find('.table-cell.c-symbol-group');
            var symbolGroup = $symbolGroupCell.text();
            if (symbolGroup !== selectedGroup) {
                $currentRow.hide();
            }
        });
    }
});

$('.scroll-to-form').on('click', function () {
    $('body,html').animate({scrollTop: $('#direction-for-green-btn-click').offset().top - 100}, 400);
});

// eslint-disable-next-line wrap-iife
(function tracking () {
    const key = 'visitor-tracking';
    if (localStorage) {
        // NOTE: Uncomment if tracking after registration is not necessary:
        // const client = localStorage.getItem('already-client');
        // if (!client) {
            const now = localStorage.getItem(key);
            let data = now ? JSON.parse(now) : [];
            let country_from = document.body.getAttribute('data-country');
            if (!country_from) {
                country_from = 'n/a';
            }
            const come_from = document.referrer;
            const come_to = location.href;
            const date = new Date().toLocaleString();
            let value = '';
            if (come_from) {
                value = `[${country_from}] from [${come_from}] to [${come_to}] at [${date}]`;
            } else {
                value = `[${country_from}] manually to [${come_to}] at [${date}]`;
            }
            data.push(value);
            localStorage.setItem(key, JSON.stringify(data));
        // }
    }
})()
