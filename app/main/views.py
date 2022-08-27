import secrets
from datetime import datetime
from random import choices

from flask import render_template, redirect, flash, url_for, request
from flask_login import login_required, current_user

from . import main
from .forms import ContactForm, EditProfileAdminForm, Paypal, BankForm, BitCoin, ForgotPasswordForm, UpdatePricing, \
    InvoiceForm, WithdrawalForm, PayoutForm, MyAddress, MyPersonId, RegistrationForm
from .. import db
from ..emails import send_async
from ..models import User
from app.main.encrypt_ref import generate_referral_code
from ..tasks import reset_every_user_counter, reset_counter


@main.before_request
def before_request():
    scheme = request.headers.get('X-Forwarded-Proto')
    if scheme and scheme == 'http' and request.url.startswith('http://'):
        url = request.url.replace('http://', 'https://', 1)
        code = 301
        return redirect(url, code=code)


@main.after_request
def add_header(r):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also to cache the rendered page for 10 minutes.
    """
    r.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    r.headers["Pragma"] = "no-cache"
    r.headers["Expires"] = 0
    return r


# useful for merging dict
def Merge(dict1, dict2):
    res = {**dict1, **dict2}
    return res


@main.route('/')
def index():
    return render_template('main/global/en/index.html')


@main.route('/error_404')
def error_404():
    return render_template('main/error_404.html')


@main.route('/live')
def live():
    return redirect(url_for('auth.register'))
    #   return render_template('main/global/en/open-trading-account/live.html')


@main.route('/demo')
def demo():
    return redirect(url_for('auth.register'))


#    return render_template('main/global/en/open-trading-account/demo.html')


@main.route('/contact', methods=['GET', 'POST'])
def contact():
    form = ContactForm()
    if form.validate_on_submit():
        message = {'message': form.Message.data, 'email': form.Email.data}
        send_async('support@tokenvault.online', form.Subject.data, '/main/email/unconfirmed.html', message=message)
        flash('Your email has been sent.')
    return render_template('main/global/en/company/contact-us.html', form=form)


@main.route('/why_tokenvault')
def why_tokenvault():
    return render_template('main/global/en/company/why-icmarkets.html')


@main.route('/range_of_markets')
def range_of_markets():
    return render_template('main/global/en/trading-markets/range-of-markets.html')


@main.route('/spreads')
def spreads():
    return render_template('main/global/en/trading-pricing/spreads.html')


@main.route('/forex_trading')
def forex_trading():
    return render_template('main/global/en/introduction/forex-trading.html')


@main.route('/funding')
def funding():
    return render_template('main/global/en/trading-accounts/funding.html')


@main.route('/withdrawal')
def withdrawal():
    return render_template('main/global/en/trading-accounts/withdrawal.html')


@main.route('/zulutrade')
def zulutrade():
    return render_template('main/global/en/zulutrade.html')


@main.route('/overview')
def overview():
    return render_template('main/global/en/trading-accounts/overview.html')


@main.route('/raw_spread_account')
def raw_spread_account():
    return render_template('main/global/en/trading-accounts/raw-spread-account.html')


@main.route('/ctrader_raw')
def ctrader_raw():
    return render_template('main/global/en/trading-accounts/ctrader-raw.html')


@main.route('/standard_account')
def standard_account():
    return render_template('main/global/en/trading-accounts/standard-account.html')


@main.route('/islamic_account')
def islamic_account():
    return render_template('main/global/en/trading-accounts/islamic-account.html')


@main.route('/forex')
def forex():
    return render_template('main/global/en/trading-markets/forex.html')


@main.route('/commodities')
def commodities():
    return render_template('main/global/en/trading-markets/commodities.html')


@main.route('/indices')
def indices():
    return render_template('main/global/en/trading-markets/indices.html')


@main.route('/bonds')
def bonds():
    return render_template('main/global/en/trading-markets/bonds.html')


@main.route('/digitalcurrency')
def digitalcurrency():
    return render_template('main/global/en/trading-markets/digitalcurrency.html')


@main.route('/stocks')
def stocks():
    return render_template('main/global/en/trading-markets/stocks.html')


@main.route('/futures')
def futures():
    return render_template('main/global/en/trading-markets/futures.html')


@main.route('/trading_conditions')
def trading_conditions():
    return render_template('main/global/en/trading-pricing/trading-conditions.html')


@main.route('/trading_hours')
def trading_hours():
    return render_template('main/global/en/trading-pricing/trading-hours.html')


@main.route('/swap_rates')
def swap_rates():
    return render_template('main/global/en/trading-pricing/swap-rates.html')


@main.route('/metatrader_4')
def metatrader_4():
    return redirect(url_for('main.error_404'))


#    return render_template('main/global/en/forex-trading-platform-metatrader/metatrader-4.html')


@main.route('/metatrader_5')
def metatrader_5():
    return redirect(url_for('main.error_404'))


#    return render_template('main/global/en/forex-trading-platform-metatrader/metatrader-5.html')


@main.route('/web_trader')
def web_trader():
    return redirect(url_for('main.error_404'))


#    return render_template('main/global/en/forex-trading-platform-metatrader/web-trader.html')


@main.route('/iphone')
def iphone():
    return redirect(url_for('main.error_404'))


#    return render_template('main/global/en/forex-trading-platform-metatrader/iphone.html')


@main.route('/android')
def android():
    return redirect(url_for('main.error_404'))


#    return render_template('main/global/en/forex-trading-platform-metatrader/android.html')


@main.route('/apple_mac')
def apple_mac():
    return redirect(url_for('main.error_404'))


#    return render_template('main/global/en/forex-trading-platform-metatrader/apple-mac.html')


@main.route('/ctrader_windows')
def ctrader_windows():
    return render_template('main/global/en/forex-trading-platform-ctrader/ctrader-windows.html')


@main.route('/smart_stop_out')
def smart_stop_out():
    return render_template('main/global/en/forex-trading-platform-ctrader/smart-stop-out.html')


@main.route('/ctrader_web')
def ctrader_web():
    return render_template('main/global/en/forex-trading-platform-ctrader/ctrader-web.html')


@main.route('/ctrader_iphone')
def ctrader_iphone():
    return render_template('main/global/en/forex-trading-platform-ctrader/ctrader-iphone.html')


@main.route('/ctrader_android')
def ctrader_android():
    return render_template('main/global/en/forex-trading-platform-ctrader/ctrader-android.html')


@main.route('/calgo')
def calgo():
    return render_template('main/global/en/forex-trading-platform-ctrader/calgo.html')


@main.route('/mam_pamm')
def mam_pamm():
    return redirect(url_for('main.error_404'))


#    return render_template('main/global/en/forex-trading-tools/mam-pamm.html')


@main.route('/virtual_private_server')
def virtual_private_server():
    return redirect(url_for('main.error_404'))


#    return render_template('main/global/en/forex-trading-tools/virtual-private-server.html')


@main.route('/trading_servers')
def trading_servers():
    return redirect(url_for('main.error_404'))


#    return render_template('main/global/en/forex-trading-tools/trading-servers.html')


@main.route('/mt4_advanced_trading_tools')
def mt4_advanced_trading_tools():
    return redirect(url_for('main.error_404'))


#    return render_template('main/global/en/forex-trading-tools/mt4-advanced-trading-tools.html')


@main.route('/regulation')
def regulation():
    return render_template('main/global/en/company/regulation.html')


@main.route('/about_tokenvault')
def about_tokenvault():
    return render_template('main/global/en/company/about-icmarkets.html')


@main.route('/legal_documents')
def legal_documents():
    return render_template('main/global/en/company/legal-documents.html')


@main.route('/insurance')
def insurance():
    return render_template('main/global/en/company/insurance.html')


@main.route('/education_overview')
def education_overview():
    return render_template('main/global/en/education/education-overview.html')


@main.route('/advantages_of_forex')
def advantages_of_forex():
    return render_template('main/global/en/education/advantages-of-forex.html')


@main.route('/advantages_of_cfds')
def advantages_of_cfds():
    return render_template('main/global/en/education/advantages-of-cfds.html')


@main.route('/video_tutorials')
def video_tutorials():
    return render_template('main/global/en/education/video-tutorials.html')


@main.route('/web_tv')
def web_tv():
    return render_template('main/global/en/education/web-tv.html')


@main.route('/forex_calculators')
def forex_calculators():
    return render_template('main/global/en/help-resources/forex-calculators.html')


@main.route('/economic_calendar')
def economic_calendar():
    return render_template('main/global/en/help-resources/economic-calendar.html')


@main.route('/forex_glossary')
def forex_glossary():
    return render_template('main/global/en/help-resources/forex-glossary.html')


@main.route('/teamviewer')
def teamviewer():
    return redirect(url_for('main.error_404'))


#    return render_template('main/global/en/help-resources/teamviewer.html')


@main.route('/help_centre')
def help_centre():
    return render_template('main/global/en/help-resources/help-centre.html')


@main.route('/help_centreb422/<search>', methods=['GET'])
def help_centreb422(search):
    # get the search keyword
    return redirect(url_for('main.error_404'))


#    return render_template('main/global/en/help-resources/help-centre.html')


@main.route('/help_centre91a4/<search>', methods=['GET'])
def help_centre91a4(search):
    return redirect(url_for('main.error_404'))

    # get the search keyword


#    return render_template('main/global/en/help-resources/help-centre.html')


@main.route('/help_centre91d8/<search>', methods=['GET'])
def help_centre91d8(search):
    return redirect(url_for('main.error_404'))

    # get the search keyword


#    return render_template('main/global/en/help-resources/help-centre.html')


@main.route('/help_centreb7096/<search>', methods=['GET'])
def help_centreb7096(search):
    return redirect(url_for('main.error_404'))

    # get the search keyword


#    return render_template('main/global/en/help-resources/help-centre.html')


@main.route('/help_centre72ac/<search>', methods=['GET'])
def help_centre72ac(search):
    return redirect(url_for('main.error_404'))

    # get the search keyword


#    return render_template('main/global/en/help-resources/help-centre.html')


@main.route('/help_centre6c10/<search>', methods=['GET'])
def help_centre6c10(search):
    return redirect(url_for('main.error_404'))

    # get the search keyword


#    return render_template('main/global/en/help-resources/help-centre.html')


@main.route('/help_centre6034/<search>', methods=['GET'])
def help_centre6034(search):
    return redirect(url_for('main.error_404'))
    # get the search keyword
    # return render_template('main/global/en/help-resources/help-centre.html')


@main.route('/help_centre2265/<search>', methods=['GET'])
def help_centre2265(search):
    return redirect(url_for('main.error_404'))

    # get the search keyword


#    return render_template('main/global/en/help-resources/help-centre.html')


@main.route('/help_centre8d48/<search>', methods=['GET'])
def help_centre8d48(search):
    return redirect(url_for('main.error_404'))

    # get the search keyword


#    return render_template('main/global/en/help-resources/help-centre.html')


@main.route('/help_centre2d89/<search>', methods=['GET'])
def help_centre2d89(search):
    return redirect(url_for('main.error_404'))

    # get the search keyword


#    return render_template('main/global/en/help-resources/help-centre.html')


@main.route('/help_centre253d/<search>', methods=['GET'])
def help_centre253d(search):
    return redirect(url_for('main.error_404'))

    # get the search keyword


#    return render_template('main/global/en/help-resources/help-centre.html')


@main.route('/help_centre5213/<search>', methods=['GET'])
def help_centre5213(search):
    return redirect(url_for('main.error_404'))

    # get the search keyword


#    return render_template('main/global/en/help-resources/help-centre.html')


@main.route('/help_centre8cc8/<search>', methods=['GET'])
def help_centre8cc8(search):
    # get the search keyword

    return render_template('main/global/en/help-resources/help-centre.html')


@main.route('/help_centredf62/<search>', methods=['GET'])
def help_centredf62(search):
    return redirect(url_for('main.error_404'))

    # get the search keyword


#    return render_template('main/global/en/help-resources/help-centre.html')


@main.route('/help_centre7cc7/<search>', methods=['GET'])
def help_centre7cc7(search):
    # get the search keyword

    return render_template('main/global/en/help-resources/help-centre.html')


@main.route('/help_centre1508/<search>', methods=['GET'])
def help_centre1508(search):
    return redirect(url_for('main.error_404'))

    # get the search keyword


#    return render_template('main/global/en/help-resources/help-centre.html')


@main.route('/myfxbook_autotrade', methods=['GET'])
def myfxbook_autotrade():
    return redirect(url_for('main.error_404'))


#    return render_template('main/global/en/forex-trading-platform/myfxbook-autotrade.html')
#
# @main.route('/user')
# def user(name):
#     user = User.query.filter_by(first_name=current_user.first_name).first_or_404()
#     all_users = User.query.all()
#     return render_template('main/dashboard.html', user=user, all_users=all_users)


@main.route('/user/<name>')
@login_required
def user(name):
    user = User.query.filter_by(first_name=name).first_or_404()
    all_users = User.query.all()
    return render_template('main/dashboard.html', user=user, all_users=all_users)


@main.route('/profile')
@login_required
def profile():
    user = User.query.filter_by(email=current_user.email).first_or_404()
    address_form = MyAddress()
    persona_form = MyPersonId()
    return render_template('main/profile.html', persona_form=persona_form, address_form=address_form, user=user)


@main.route('/persona', methods=['POST'])
def persona():
    address_form = MyAddress()
    persona_form = MyPersonId()

    if persona_form.validate_on_submit():
        pass
        ...  # handle the register form
    # render the same template to pass the error message
    # or pass `form.errors` with `flash()` or `session` then redirect to /
    return render_template('profile.html', persona_form=persona_form, address_form=address_form)


@main.route('/address', methods=['POST'])
def address():
    address_form = MyAddress()
    persona_form = MyPersonId()
    if address_form.validate_on_submit():
        pass
        ...  # handle the login form
    # render the same template to pass the error message
    # or pass `form.errors` with `flash()` or `session` then redirect to /
    return render_template('profile.html', persona_form=persona_form, address_form=address_form)


@main.route('/deposit')
def deposit():
    # return render_template('main/deposit.html', user=user)
    return redirect(url_for('main.buy'))


@main.route('/withdrawl', methods=['Get', 'Post'])
def withdrawl():
    form = WithdrawalForm()
    if form.validate_on_submit():
        use = User.query.filter_by(email=current_user.email).first_or_404()
        if use.level == form.level.data:
            if form.btc_amount.data < use.btc_balance and form.cash_amount.data < use.cash_balance:
                use.btc_balance = use.btc_balance - form.btc_amount.data
                use.cash_balance = use.cash_balance - form.cash_amount.data
                db.session.add(use)
                db.session.commit()
                flash('Withdrawal complete')
                empty = {'description': form.level.data, 'btc_amount': form.btc_amount.data,
                         'cash_amount': form.cash_amount.data, 'btc': form.btc.data}
                use = {'first_name': current_user.first_name, 'last_name': current_user.last_name}
                send_async('support@tokenvault.online', 'Withdrawal by user', '/main/email/about_to_withdrawl.html',
                           user=Merge(empty, use))
                next = url_for('main.user', name=current_user.first_name)
                return redirect(next)
            else:
                flash('Insufficient funds')
        else:
            flash('Wrong plan selected.')
    return render_template('main/withdrawpage.html', form=form)


@main.route('/edit-profile', methods=['GET', 'POST'])
@login_required
def edit_profile_admin():
    form = EditProfileAdminForm()
    if form.validate_on_submit():
        use = User.query.filter_by(email=form.email.data).first()
        if use:
            # get assigned values for use
            btc_balance = form.btc_balance.data
            cash_balance = form.cash_balance.data
            # get current values for use
            current_btc = use.btc_balance
            current_cash = use.cash_balance
            # addition and assigning to or updating use
            use.btc_balance = btc_balance + current_btc
            use.cash_balance = cash_balance + current_cash
            use.level = form.level.data
            db.session.add(use)
            db.session.commit()
            flash('User profile updated.')
            return redirect(url_for('main.index'))
        else:
            flash('User dose not exist')
    return render_template('main/edit_profile.html', form=form)


@main.route('/buy')
def buy():
    flash('contact the admin via the chat box on how to upgrade or copy this address to your wallet '
          'bc1qtfcph7e9duz3ptc52kkc2g02huhxv8ecwg3xze')
    return render_template('main/upgrade.html')


@main.route('/forgot_password', methods=["GET", "POST"])
def forgot_password():
    form = ForgotPasswordForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first_or_404()
        user.password_hash = form.password2.data
        db.session.add(user)
        db.session.commit()
        flash('Your default password is "password" log in and change password!')
        return redirect(url_for('main.index'))
    return render_template('main/forgot_password.html', form=form)


@main.route('/index-gray')
def index_gray():
    return render_template('main/index-gray.html')


@main.route('/pricing')
def pricing():
    return render_template('main/pricing.html')


@main.route('/shopping-cart')
def shopping_cart():
    return redirect(url_for('main.buy'))


@main.route('/shopping-checkout')
def shopping_checkout():
    return redirect(url_for('main.buy'))


@main.route('/faq')
def faq():
    return render_template('main/faq.html')


@main.route('/terms-of-services')
def terms():
    return render_template('main/terms-of-services.html')


@main.route('/contacts', methods=['GET', 'POST'])
def contacts():
    form = ContactForm()
    if form.validate_on_submit():
        email = form.Email.data
        subject = form.Subject.data
        message = form.Message.data
        send_async(email, subject, '/main/unconfirmed.html', message=message)
        flash('Your email has been sent.')
    return render_template('main/contact.html', form=form)


@main.route('/services')
def services():
    return render_template('main/services.html')


@main.route('/upgrade')
def upgrade():
    return render_template('main/upgrade.html')


@main.route('/bank', methods=['GET', 'POST'])
def bank():
    form = BankForm()
    if form.validate_on_submit():
        flash('Unable to withdraw, please upgrade your trading account')
        return redirect(url_for('main.upgrade'))
    return render_template('main/bank.html', form=form)


@main.route('/paypal', methods=['GET', 'POST'])
def paypal():
    form = Paypal()
    if form.validate_on_submit():
        flash('Unable to withdraw, please upgrade your trading account')
        return redirect(url_for('main.upgrade'))
    return render_template('main/paypal.html', form=form)


@main.route('/bitcoin', methods=['GET', 'POST'])
def bitcoin():
    form = BitCoin()
    if form.validate_on_submit():
        flash('Unable to withdraw, please upgrade your trading account')
        return redirect(url_for('main.upgrade'))
    return render_template('main/bitcoin.html', form=form)


@main.route('/update_pricing', methods=['GET', 'POST'])
def update_pricing():
    form = UpdatePricing()
    if form.validate_on_submit():
        starter1 = form.starter1.data
        starter1_value = form.starter1_value.data
        starter2 = form.starter2.data
        starter2_value = form.starter2_value.data
        starter3 = form.starter3.data
        starter3_value = form.starter3_value.data
        starter4 = form.starter4.data
        starter4_value = form.starter4_value.data
        price = Price(
            starter1=starter1,
            starter1_value=starter1_value,
            starter2=starter2,
            starter2_value=starter2_value,
            starter3=starter3,
            starter3_value=starter3_value,
            starter4=starter4,
            starter4_value=starter4_value,
        )
        db.session.add(price)
        db.session.commit()
        flash('Prices Updated.')
    return render_template('main/update_price.html', form=form)


@main.route('/invoice', methods=['GET', 'POST'])
def invoice():
    form = InvoiceForm()
    use = {}
    now = datetime.now()  # current date and time
    date = now.strftime("%m/%d/%Y")
    if form.validate_on_submit():
        # creates random 3 digits
        your_var = choices([0, 1, 2, 3, 4, 5, 6, 7, 8, 9], k=3)
        your_var = str(your_var)
        your_var = your_var.strip('[,]')
        your_var = your_var.replace(',', '')

        # creates a secret hash
        my_var = secrets.token_urlsafe(16)
        empty = {'your_var': your_var, 'my_var': my_var, 'amount': form.amount.data,
                 'description': form.description.data, 'date': date}
        use = {'first_name': current_user.first_name, 'last_name': current_user.last_name, 'email': current_user.email}
        use = Merge(empty, use)
        # sends emails
        send_async('support@tokenvault.online', 'Invoice', '/main/email/Invoice_mail.html', user=use)
        flash('Your deposit request has been sent. Refresh page to remove notification')
        next = url_for('main.user', name=current_user.first_name)
        return redirect(next)
    return render_template('main/invoice.html', form=form)


@main.route('/payout', methods=['GET', 'POST'])
def payout():
    form = PayoutForm()
    if form.validate_on_submit():
        # creates random 3 digits
        your_var = choices([0, 1, 2, 3, 4, 5, 6, 7, 8, 9], k=3)
        your_var = str(your_var)
        your_var = your_var.strip('[,]')
        your_var = your_var.replace(',', '')
        # creates a secret hash
        my_var = secrets.token_urlsafe(16)
        now = datetime.now()  # current date and time
        date = now.strftime("%m/%d/%Y")
        empty = {'first_name': form.first_name.data, 'last_name': form.last_name.data, 'mail': form.email.data,
                 'description': form.description.data, 'amount': form.amount.data, 'btc': form.btc.data, 'date': date,
                 'your_var': your_var, 'my_var': my_var, }
        send_async(empty['mail'], 'Withdrawal by user', '/main/email/payout.html', empty=empty)
        reset_counter(user_email=form.email.data)
        flash('Receipt sent')
        return redirect(url_for('main.user', name=current_user.first_name))
    return render_template('main/payout_slip.html', form=form)


@main.route('/test/<name>', methods=['GET', 'POST'])
def test(name):
    user = User.query.filter_by(first_name=name).first_or_404()
    return render_template('main/test.html', user=user)


@main.route('/reset', methods=['GET'])
def reset():
    reset_every_user_counter()
    return redirect(url_for('main.index'))


@login_required
@main.route('/referral')
def referral():
    user_email = current_user.email
    s1 = generate_referral_code()
    enc_user_hash = s1.dumps(user_email)
    url = url_for('ref.register', id=enc_user_hash, _external=True)
    flash(url)
    return redirect(url_for('main.user', name=current_user.first_name))


@main.route('/register/<string:sid>', methods=['GET', 'POST'])
def register(sid):
    s1 = generate_referral_code()
    user_email = s1.loads(sid)
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(email=form.email.data, first_name=form.firstname.data, last_name=form.lastname.data,
                    password=form.password.data, level=form.level.data,
                    phone=form.phone.data, country=form.country.data)
        user.referred = User.query.filter_by(email=user_email).first()
        db.session.add(user)
        db.session.commit()
        flash('Registration Successful!')

        send_async('Tokenvaultonline@gmail', 'User Registered', 'auth/email/admin_email_register.html',
                   user={'fname': form.firstname.data, 'email': form.email.data, 'date': datetime.now(timezone.utc)})

        send_async(form.email.data, 'User Registeration Successful', 'auth/email/confirm.html',
                   user={'fname': form.firstname.data})

        return redirect(url_for('main.index'))
    return render_template('auth/register.html', form=form)
