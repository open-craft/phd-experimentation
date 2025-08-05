

function addPlugins(config, slot_name, plugins) {
  if (slot_name in config.pluginSlots === false) {
    config.pluginSlots[slot_name] = {
      keepDefault: true,
      plugins: []
    };
  }

  config.pluginSlots[slot_name].plugins.push(...plugins);
}

async function setConfig () {
  let config = {
    pluginSlots: {}
  };

  try {
    /* We can't assume FPF exists, as it's not declared as a dependency in all
     * MFEs, so we import it dynamically. In addition, for dynamic imports to
     * work with Webpack all of the code that actually uses the imported module
     * needs to be inside the `try{}` block.
     */
    const { DIRECT_PLUGIN, PLUGIN_OPERATIONS } = await import('@openedx/frontend-plugin-framework');
    if (process.env.APP_ID == 'authn') {
    }
    if (process.env.APP_ID == 'authoring') {

      // Currently there is no way to conditionally add plugin slot configuration from tutor-mfe.
      // So, as a workaround, tutor-contrib-aspects simply defines the components added to the plugin as empty components.
      const CourseOutlineSidebar = () => {};
      const UnitPageSidebar = () => {};
      const SidebarToggleWrapper = () => {};
      const CourseHeaderButton = () => {};
      const UnitActionsButton = () => {};
      const SubSectionAnalyticsButton = () => {};

      addPlugins(config, 'course_authoring_outline_sidebar_slot', [
          {
            op: PLUGIN_OPERATIONS.Insert,
            widget: {
                id: 'outline-sidebar',
                priority: 1,
                type: DIRECT_PLUGIN,
                RenderWidget: CourseOutlineSidebar,
            },
          }]);
      addPlugins(config, 'course_authoring_outline_sidebar_slot', [
          {
            op: PLUGIN_OPERATIONS.Wrap,
            widgetId: 'default_contents',
            wrapper: SidebarToggleWrapper,
          }]);
      addPlugins(config, 'course_authoring_unit_sidebar_slot', [
          {
            op: PLUGIN_OPERATIONS.Insert,
            widget: {
                id: 'course-unit-sidebar',
                priority: 1,
                type: DIRECT_PLUGIN,
                RenderWidget: UnitPageSidebar,
            },
          }]);
      addPlugins(config, 'course_authoring_unit_sidebar_slot', [
          {
            op: PLUGIN_OPERATIONS.Wrap,
            widgetId: 'default_contents',
            wrapper: SidebarToggleWrapper,
          }]);
      addPlugins(config, 'course_unit_header_actions_slot', [
          {
              op: PLUGIN_OPERATIONS.Insert,
              widget: {
                  id: 'unit-header-aspects-button',
                  priority: 60,
                  type: DIRECT_PLUGIN,
                  RenderWidget: CourseHeaderButton,
              },
          }]);
      addPlugins(config, 'course_outline_header_actions_slot', [
          {
              op: PLUGIN_OPERATIONS.Insert,
              widget: {
                  id: 'outline-header-aspects-button',
                  priority: 60,
                  type: DIRECT_PLUGIN,
                  RenderWidget: CourseHeaderButton,
              },
          }]);
      addPlugins(config, 'course_outline_unit_card_extra_actions_slot', [
          {
            op: PLUGIN_OPERATIONS.Insert,
            widget: {
                id: 'units-action-aspects-button',
                priority: 60,
                type: DIRECT_PLUGIN,
                RenderWidget: UnitActionsButton,
            },
          }]);
      addPlugins(config, 'course_outline_subsection_card_extra_actions_slot', [
          {
            op: PLUGIN_OPERATIONS.Insert,
            widget: {
                id: 'units-action-aspects-button',
                priority: 60,
                type: DIRECT_PLUGIN,
                RenderWidget: SubSectionAnalyticsButton,
            },
          }]);
    }
    if (process.env.APP_ID == 'account') {
    }
    if (process.env.APP_ID == 'communications') {
    }
    if (process.env.APP_ID == 'discussions') {
    }
    if (process.env.APP_ID == 'gradebook') {
    }
    if (process.env.APP_ID == 'learner-dashboard') {
    }
    if (process.env.APP_ID == 'learning') {
    }
    if (process.env.APP_ID == 'ora-grading') {
    }
    if (process.env.APP_ID == 'profile') {
    }
  } catch (err) { console.error("env.config.jsx failed to apply: ", err);}

  return config;
}

export default setConfig;