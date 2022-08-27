// Initialize Zendesk Chat widget
function initZendeskChat(branchId, locale, t, passedName, passedEmail, from) {
  const isNonChinese = (locale && locale !== "zh-cn") || (from && from === "gca");
  // Initialize variables
  const DEPARTMENTS = {
    CHATBOT: t ? t.DEPARTMENTS_CHATBOT : "ChatBot",
    GLOBAL_SUPPORT: t ? t.DEPARTMENTS_GLOBAL_SUPPORT : "Global Support",
    CHINESE_SUPPORT: t ? t.DEPARTMENTS_CHINESE_SUPPORT : "Chinese Support",
    ASIC: t ? t.DEPARTMENTS_ASIC : "Support - ASIC",
    CYSEC: t ? t.DEPARTMENTS_CYSEC : "Support - EU",
    FSA: t ? t.DEPARTMENTS_FSA : "Support - FSA",
    SCB: t ? t.DEPARTMENTS_SCB : "Support - SCB",
  };
  const DEPARTMENT_STATUS = {
    ONLINE: t ? t.STATUS_ONLINE : "online",
    OFFLINE: t ? t.STATUS_OFFLINE : "offline",
  };
  const GREETING = {
    ASIC: t
      ? t.GREETING_ASIC
      : from === "gca"
      ? "By starting the live chat, you agree that your personal data, provided via chat, will be processed by IC Markets in accordance with its Privacy Policy for the purpose of providing support as requested by you. The data collected will be processed only during the time needed to carry out the service unless otherwise determined by applicable law."
      : "开始即时会话前，您同意 IC Markets 遵照隐私政策处理您在会话中提供的个人信息、为您提供支持。在无相关法律干涉的情况下，这些个人信息仅会在服务期间被收集和处理。",
    CYSEC: t
      ? t.GREETING_CYSEC
      : from === "gca"
      ? "By starting the live chat, you agree that your personal data, provided via chat, will be processed by IC Markets (EU) in accordance with its Privacy Policy for the purpose of providing support as requested by you. The data collected will be processed only during the time needed to carry out the service unless otherwise determined by applicable law."
      : "开始即时会话前，您同意 IC Markets (EU) 遵照隐私政策处理您在会话中提供的个人信息、为您提供支持。在无相关法律干涉的情况下，这些个人信息仅会在服务期间被收集和处理。",
    FSA: t
      ? t.GREETING_FSA
      : from === "gca"
      ? "By starting the live chat, you agree that your personal data, provided via chat, will be processed by IC Markets in accordance with its Privacy Policy for the purpose of providing support as requested by you. The data collected will be processed only during the time needed to carry out the service unless otherwise determined by applicable law."
      : "开始即时会话前，您同意 IC Markets 遵照隐私政策处理您在会话中提供的个人信息、为您提供支持。在无相关法律干涉的情况下，这些个人信息仅会在服务期间被收集和处理。",
    SCB: t
      ? t.GREETING_SCB
      : from === "gca"
      ? "By starting the live chat, you agree that your personal data, provided via chat, will be processed by IC Markets (BS) in accordance with its Privacy Policy for the purpose of providing support as requested by you. The data collected will be processed only during the time needed to carry out the service unless otherwise determined by applicable law."
      : "开始即时会话前，您同意 IC Markets (BS) 遵照隐私政策处理您在会话中提供的个人信息、为您提供支持。在无相关法律干涉的情况下，这些个人信息仅会在服务期间被收集和处理。",
  };
  const TITLE_NO_CHAT = {
    ASIC: t ? t.TITLE_NO_CHAT_ASIC : from === "gca" ? "IC Markets Support" : "IC Markets 客户支持",
    CYSEC: t ? t.TITLE_NO_CHAT_CYSEC : from === "gca" ? "IC Markets (EU) Support" : "IC Markets (EU) 客户支持",
    FSA: t ? t.TITLE_NO_CHAT_FSA : from === "gca" ? "IC Markets Global Support" : "IC Markets 客户支持",
    SCB: t
      ? t.TITLE_NO_CHAT_SCB
      : from === "gca"
      ? "IC Markets International Support"
      : "IC Markets International 客户支持",
  };
  const TITLE_CHAT = {
    ASIC: t ? t.TITLE_CHAT_ASIC : from === "gca" ? "IC Markets Live Chat" : "IC Markets 在线聊天",
    CYSEC: t ? t.TITLE_CHAT_CYSEC : from === "gca" ? "IC Markets (EU) Live Chat" : "IC Markets (EU) 在线聊天",
    FSA: t ? t.TITLE_CHAT_FSA : from === "gca" ? "IC Markets Global Live Chat" : "IC Markets 在线聊天",
    SCB: t
      ? t.TITLE_CHAT_SCB
      : from === "gca"
      ? "IC Markets International Live Chat"
      : "IC Markets International 在线聊天",
  };
  const TITLE_ANSWERBOT = {
    ASIC: t ? t.TITLE_ANSWERBOT_ASIC : "IC Markets",
    CYSEC: t ? t.TITLE_ANSWERBOT_CYSEC : "IC Markets (EU)",
    FSA: t ? t.TITLE_ANSWERBOT_FSA : "IC Markets",
    SCB: t ? t.TITLE_ANSWERBOT_SCB : "IC Markets International",
  };
  const CONTACT_OPTIONS = {
    CONTACT_BUTTON: t ? t.contactButton : from === "gca" ? "Get in touch" : "开始会话",
    CHAT_LABEL_ONLINE: t ? t.chatLabelOnline : from === "gca" ? "Chat with us" : "与我们对话",
    CHAT_LABEL_OFFLINE: t ? t.chatLabelOffline : from === "gca" ? "Chat is unavailable" : "暂无法开始会话",
    CONTACT_FORM_LABEL: t ? t.contactFormLabel : from === "gca" ? "Leave us a message" : "给我们留言",
  };
  const HI = t ? t.Hi : from === "gca" ? "Hi" : "你好";

  var cssId = "zendeskCustomCss";
  var greeting, titleNoChat, titleChat, titleAnswerBot, departmentBasedOnPassedBranch, departments, chatBotOnline;

  switch (branchId) {
    case 4: // BS (SCB)
      departmentBasedOnPassedBranch = DEPARTMENTS.SCB;
      greeting = GREETING.SCB;
      titleNoChat = TITLE_NO_CHAT.SCB;
      titleChat = TITLE_CHAT.SCB;
      titleAnswerBot = TITLE_ANSWERBOT.SCB;
      break;
    case 3: // SC (FSA)
      departmentBasedOnPassedBranch = DEPARTMENTS.FSA;
      greeting = GREETING.FSA;
      titleNoChat = TITLE_NO_CHAT.FSA;
      titleChat = TITLE_CHAT.FSA;
      titleAnswerBot = TITLE_ANSWERBOT.FSA;
      break;
    case 2: // EU (CySEC)
      departmentBasedOnPassedBranch = DEPARTMENTS.CYSEC;
      greeting = GREETING.CYSEC;
      titleNoChat = TITLE_NO_CHAT.CYSEC;
      titleChat = TITLE_CHAT.CYSEC;
      titleAnswerBot = TITLE_ANSWERBOT.CYSEC;
      break;
    case 1: // AU (ASIC)
    default:
      departmentBasedOnPassedBranch = DEPARTMENTS.ASIC;
      greeting = GREETING.ASIC;
      titleNoChat = TITLE_NO_CHAT.ASIC;
      titleChat = TITLE_CHAT.ASIC;
      titleAnswerBot = TITLE_ANSWERBOT.ASIC;
  }

  //Zendesk chat widget setting
  window.zESettings = {
    webWidget: {
      answerBot: {
        suppress: false,
        title: {
          "*": titleNoChat,
        },
        avatar: {
          url: "https://chatwidget.icmarkets-resources.com/assets/circle-logo-white.png",
          name: {
            "*": titleAnswerBot,
          },
        },
        contactOnlyAfterQuery: true,
      },
      chat: {
        suppress: false,
        title: {
          "*": titleChat,
          // },
          // prechatForm: {
          //     greeting: {
          //         '*': greeting
          //     }
        },
        departments: {
          enabled: [isNonChinese ? departmentBasedOnPassedBranch : DEPARTMENTS.CHINESE_SUPPORT],
          select: isNonChinese ? departmentBasedOnPassedBranch : DEPARTMENTS.CHINESE_SUPPORT,
        },
      },
      contactOptions: {
        enabled: false,
        contactButton: { "*": CONTACT_OPTIONS.CONTACT_BUTTON },
        chatLabelOnline: { "*": CONTACT_OPTIONS.CHAT_LABEL_ONLINE },
        chatLabelOffline: { "*": CONTACT_OPTIONS.CHAT_LABEL_OFFLINE },
        contactFormLabel: { "*": CONTACT_OPTIONS.CONTACT_FORM_LABEL },
      },
      launcher: {
        mobile: {
          labelVisible: false,
        },
      },
      navigation: {
        popoutButton: {
          enabled: false,
        },
      },
    },
  };

  window.zE(function () {
    //set locale
    if (locale) {
      window.zE("webWidget", "setLocale", locale);
    } else if (from === "cca") {
      window.zE("webWidget", "setLocale", "zh-cn");
    }

    //prefill user details
    if (passedName && passedEmail) {
      window.zE("webWidget", "prefill", {
        name: {
          value: passedName,
        },
        email: {
          value: passedEmail,
        },
      });
    }

    window.zE("webWidget:on", "open", function () {
      //Load css file when Zendesk chat is opened for the first time
      var checkExist = setInterval(() => {
        var iframes = $("iframe");
        for (let i = 0; i < iframes.length; i++) {
          if (iframes[i].id === "webWidget") {
            if (!iframes[i].contentDocument.getElementById(cssId)) {
              var head = iframes[i].contentDocument.getElementsByTagName("head")[0];
              var link = iframes[i].contentDocument.createElement("link");
              link.id = cssId;
              link.rel = "stylesheet";
              link.type = "text/css";
              link.href = "https://chatwidget.icmarkets-resources.com/assets/zendeskChat.css";
              link.media = "all";
              head.appendChild(link);
            }
            clearInterval(checkExist);
          }
        }
      }, 100);
    });

    window.zE("webWidget:on", "chat:connected", function () {
      setTimeout(() => {
        //Get departments
        departments = window.zE("webWidget:get", "chat:departments");

        chatBotOnline = false;
        if (
          isNonChinese &&
          departments.find((d) => d.name === DEPARTMENTS.CHATBOT && d.status === DEPARTMENT_STATUS.ONLINE)
        ) {
          chatBotOnline = true;
        }

        var supportOnline = false;
        if (isNonChinese) {
          if (
            departments.find((d) => d.name === departmentBasedOnPassedBranch && d.status === DEPARTMENT_STATUS.ONLINE)
          ) {
            supportOnline = true;
          }
        } else {
          if (
            departments.find((d) => d.name === DEPARTMENTS.CHINESE_SUPPORT && d.status === DEPARTMENT_STATUS.ONLINE)
          ) {
            supportOnline = true;
          }
        }

        // Assign the chat to ChatBot department
        if (chatBotOnline) {
          window.zE("webWidget", "updateSettings", {
            webWidget: {
              chat: {
                departments: {
                  enabled: [DEPARTMENTS.CHATBOT],
                  select: DEPARTMENTS.CHATBOT,
                },
              },
            },
          });

          if (isNonChinese) {
            window.zE("webWidget", "updatePath", {
              title: "department=" + departmentBasedOnPassedBranch,
              url: "https://example.com/?department=" + departmentBasedOnPassedBranch,
            });
          }
        }
        // Assign the chat to Support department
        else if (supportOnline) {
          window.zE("webWidget", "updateSettings", {
            webWidget: {
              chat: {
                departments: {
                  enabled: [isNonChinese ? departmentBasedOnPassedBranch : DEPARTMENTS.CHINESE_SUPPORT],
                  select: isNonChinese ? departmentBasedOnPassedBranch : DEPARTMENTS.CHINESE_SUPPORT,
                },
              },
            },
          });
        }
        // Disable Chat to display Contact form
        else {
          window.zE("webWidget", "updateSettings", {
            webWidget: {
              chat: {
                suppress: true,
              },
            },
          });
        }
      }, 500);
    });

    window.zE("webWidget:on", "userEvent", function (event) {
      if (event.category === "Zendesk Web Widget" && event.action === "Chat Request Form Submitted") {
        if ((passedName && passedEmail) || locale === "zh-cn") {
          if (
            document.querySelector("iframe#webWidget").contentDocument.querySelector("textarea").value.trim() === ""
          ) {
            sendHi();
          }
        } else {
          var email = document
            .querySelector("iframe#webWidget")
            .contentDocument.querySelector("input[name=email]").value;

          $.ajaxSetup({
            headers: {
              Authorization: `Bearer ${window.jwt}`,
            },
          });

          $.get("https://apigateway.icmarkets.com/customers?email=" + email)
            .done(function (result) {
              var actualDepartment;

              switch (result.branch.name) {
                case "ASIC":
                  actualDepartment = DEPARTMENTS.ASIC;
                  break;

                case "CySEC":
                  actualDepartment = DEPARTMENTS.CYSEC;
                  break;

                case "FSA":
                  actualDepartment = DEPARTMENTS.FSA;
                  break;

                case "SCB":
                  actualDepartment = DEPARTMENTS.SCB;
                  break;
              }

              if (actualDepartment !== departmentBasedOnPassedBranch) {
                if (chatBotOnline) {
                  window.zE("webWidget", "updatePath", {
                    title: "department=" + actualDepartment,
                    url: "https://example.com/actual/?department=" + actualDepartment,
                  });

                  sendHi();
                } else if (
                  departments.find((d) => d.name === actualDepartment && d.status === DEPARTMENT_STATUS.ONLINE)
                ) {
                  window.zE("webWidget", "updateSettings", {
                    webWidget: {
                      chat: {
                        departments: {
                          enabled: [actualDepartment],
                          select: actualDepartment,
                        },
                      },
                    },
                  });

                  sendHi();
                } else {
                  window.zE("webWidget", "updateSettings", {
                    webWidget: {
                      chat: {
                        suppress: true,
                      },
                    },
                  });
                }
              } else {
                sendHi();
              }
            })
            .fail(function (fail) {
              sendHi();
            });
        }
      }
    });
  });

  function sendHi() {
    // window.zE("webWidget", "chat:send", HI);

    document.querySelector("iframe#webWidget").contentDocument.querySelector("textarea").style.visibility = "visible";
  }
}

//open Zendesk Chat widget
function openChatWidget() {
  zE("webWidget", "open");
}
